import os
import logging
import time
import hashlib
import json
import google.cloud.pubsub_v1
import google.cloud.firestore
import reusable
from argparse import Namespace
from copy import deepcopy
from flask import make_response
from version import VERSION
from app import utils as ut
from app import interactivity as inter
from app.game import Game

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level='INFO')
logger = logging.getLogger()

context = Namespace()
context.project_id = os.getenv('PROJECT_ID')
context.surface_prefix = hashlib.md5(context.project_id.encode()).hexdigest()
context.publisher = google.cloud.pubsub_v1.PublisherClient()
context.db = google.cloud.firestore.Client(project=context.project_id)


def build_game(game_id):
    return Game(
        game_id=game_id,
        surface_prefix=context.surface_prefix,
        project_id=context.project_id,
        publisher=context.publisher,
        db=context.db)


context.build_game_func = build_game


def slash_command(request):
    body = request.get_data()
    headers = request.headers
    form = request.form
    team_id = form['team_id']
    channel_id = form['channel_id']
    organizer_id = form['user_id']
    trigger_id = form['trigger_id']
    text = form['text']
    slash_datetime_compact = reusable.time.get_now_compact_format()
    game_id = ut.ids.build_game_id(
        slash_datetime_compact, team_id, channel_id, organizer_id, trigger_id)
    logger.info(f'game_id built, game_id={game_id}')
    game = build_game(game_id=game_id)
    ut.exceptions.ExceptionsHandler(game).verify_signature(body, headers)
    game.version = VERSION
    text_split = text.split(' ')
    parameter = text_split[0]
    tag = ''
    if len(text_split) > 1:
        tag = text_split[1]
    game.parameter = parameter
    game.tag = tag
    game.dict = dict()
    for attribute in ['version', 'parameter', 'tag']:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=False)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_slash_command_exceptions(trigger_id)
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    if game.parameter == 'help':
        ut.slack.SlackOperator(game).send_help(organizer_id)
    elif game.parameter == 'freestyle':
        ut.slack.SlackOperator(game).open_setup_freestyle_view(trigger_id)
    elif game.parameter in ('english', 'french'):
        url, questions_answers = ut.questions.get_data(game)
        max_number, number, question, answer = ut.questions.select(
            questions_answers)
        ut.slack.SlackOperator(game).open_setup_automatic_view(
            trigger_id, url, max_number, number, question, answer)
    logger.info(f'setup_view opened, game_id={game.id}')
    return make_response('', 200)


def interactivity(request):
    body = request.get_data()
    headers = request.headers
    form = request.form
    payload = json.loads(form['payload'])
    payload_type = payload['type']
    if payload_type not in ('view_submission', 'block_actions'):
        return make_response('', 200)
    if payload_type == 'view_submission':
        return inter.view_submissions.handle_view_submission(
            body, headers, payload, context)
    if payload_type == 'block_actions':
        return inter.block_actions.handle_block_action(
            body, headers, payload, context)


def pre_guess_stage(event, context_):
    assert context_ == context_

    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_guess_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['pre_guess_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    slack_operator = ut.slack.SlackOperator(game)
    game.upper_ts, game.lower_ts = slack_operator.post_pre_guess_stage()
    game.nb_members = slack_operator.get_conversation_infos()['num_members']
    max_guessers = game.nb_members - 1
    if game.parameter == 'freestyle':
        max_guessers -= 1
    max_guessers = min(max_guessers, game.max_guessers_per_game)
    game.max_guessers = max_guessers
    game.guessers = dict()
    game.guess_start = reusable.time.get_now()
    game.guess_deadline = ut.time.compute_deadline(
        game.guess_start, game.time_to_guess)
    for attribute in [
        'upper_ts',
        'lower_ts',
        'nb_members',
        'max_guessers',
        'guessers',
        'guess_start',
        'guess_deadline'
    ]:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    game = build_game(game_id)
    ut.slack.SlackOperator(game).update_guess_stage()
    game.stage_triggerer.trigger_guess_stage()
    logger.info(f'guess_stage triggered, game_id={game_id}')
    return make_response('', 200)


def guess_stage(event, context_):
    assert context_ == context_
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_guess_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['guess_stage_last_trigger'] = reusable.time.get_now()
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    while True:
        game = build_game(game_id)
        ut.slack.SlackOperator(game).update_guess_stage_lower()
        c1 = game.time_left_to_guess <= 0
        c2 = game.nb_remaining_potential_guessers <= 0
        if c1 or c2:
            game.dict['frozen_guessers'] = deepcopy(game.dict['guessers'])
            game.dict['guess_stage_over'] = True
            ut.firestore.FirestoreEditor(game).set_game(merge=True)
            game.stage_triggerer.trigger_pre_vote_stage()
            logger.info(f'pre_vote_stage triggered, game_id={game_id}')
            return make_response('', 200)
        if ut.time.datetime1_minus_datetime2(
                reusable.time.get_now(), call_datetime) > \
                game.self_trigger_threshold:
            game.stage_triggerer.trigger_guess_stage()
            logger.info(f'guess_stage self-triggered, game_id={game_id}')
            return make_response('', 200)
        time.sleep(game.refresh_interval)


def pre_vote_stage(event, context_):
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_vote_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['pre_vote_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    ut.slack.SlackOperator(game).update_pre_vote_stage()

    game.indexed_signed_proposals = \
        ut.proposals.build_indexed_signed_proposals(game)
    proposals_browser = ut.proposals.ProposalsBrowser(game)
    game.truth_index = proposals_browser.compute_truth_index()
    game.potential_voters = game.frozen_guessers
    game.voters = dict()
    game.vote_start = reusable.time.get_now()
    game.vote_deadline = ut.time.compute_deadline(
        game.vote_start, game.time_to_vote)
    for attribute in [
        'indexed_signed_proposals',
        'truth_index',
        'potential_voters',
        'voters',
        'vote_start',
        'vote_deadline'
    ]:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    game = build_game(game_id)
    slack_operator = ut.slack.SlackOperator(game)
    slack_operator.update_vote_stage()
    slack_operator.send_vote_reminders()
    game.stage_triggerer.trigger_vote_stage()
    logger.info(f'vote_stage triggered, game_id={game_id}')
    return make_response('', 200)


def vote_stage(event, context_):
    assert context_ == context_
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(game).handle_vote_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['vote_stage_last_trigger'] = reusable.time.get_now()
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    while True:
        game = build_game(game_id)
        ut.slack.SlackOperator(game).update_vote_stage_lower()
        c1 = len(game.frozen_guessers) == 1
        c2 = game.time_left_to_vote <= 0
        c3 = not game.remaining_potential_voters
        if c1 or c2 or c3:
            game.dict['frozen_voters'] = deepcopy(game.dict['voters'])
            game.dict['vote_stage_over'] = True
            ut.firestore.FirestoreEditor(game).set_game(merge=True)
            game.stage_triggerer.trigger_pre_result_stage()
            logger.info(f'pre_result_stage triggered, game_id={game_id}')
            return make_response('', 200)
        if ut.time.datetime1_minus_datetime2(
                reusable.time.get_now(),
                call_datetime) > game.self_trigger_threshold:
            game.stage_triggerer.trigger_vote_stage()
            logger.info(f'vote_stage self-triggered, game_id={game_id}')
            return make_response('', 200)
        time.sleep(game.refresh_interval)


def pre_result_stage(event, context_):
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_results_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['pre_result_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    ut.slack.SlackOperator(game).update_pre_result_stage()

    game.results = ut.results.ResultsBuilder(game).build_results()
    game.max_score = ut.results.compute_max_score(game)
    game.winners = ut.results.compute_winners(game)
    for attribute in ['results', 'max_score', 'winners']:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    slack_operator = ut.slack.SlackOperator(game)
    slack_operator.update_result_stage()
    slack_operator.send_is_over_notifications()
    game.stage_triggerer.trigger_result_stage()
    logger.info(f'result_stage triggered, game_id={game_id}')
    return make_response('', 200)


def result_stage(event, context_):
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_results_stage_exceptions()
    if resp is not None:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['result_stage_over'] = True
    firestore_editor = ut.firestore.FirestoreEditor(game)
    firestore_editor.set_game(merge=True)
    logger.info(f'sucessfully ended, game_id={game_id}')
    return make_response('', 200)


def freeze(event, context_):
    assert event == event and context_ == context_
    teams_ref = context.db.collection('teams')
    for t in teams_ref.stream():
        team_ref = teams_ref.document(t.id)
        team_dict = team_ref.get().to_dict()
        games_ref = team_ref.collection('games')
        for g in games_ref.stream():
            game_id = g.id
            game_dict = g.to_dict()
            if ut.exceptions.game_is_too_old(
                    game_id, team_dict['max_life_span']):
                if 'result_stage_over' in game_dict:
                    ref = context.db.collection('successes').document(game_id)
                    kind = 'success'
                elif sorted(game_dict.keys()) == [
                        'parameter', 'tag', 'version']:
                    ref = context.db.collection('unsubmitteds').document(
                        game_id)
                    kind = 'unsubmitted'
                else:
                    ref = context.db.collection('fails').document(game_id)
                    kind = 'fail'
                ref.set(game_dict, merge=False)
                g.reference.delete()
                logger.info(f'{kind} frozen, game_id={g.id}')
    return make_response('', 200)
