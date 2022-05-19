import os
import logging
import time
import hashlib
import json
import google.cloud.pubsub_v1
import google.cloud.firestore
import google.cloud.storage
import reusable
from copy import deepcopy
from flask import make_response
from app import utils as ut
from app import message_actions as ma
from app.game import Game

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level='INFO')
logger = logging.getLogger()

project_id = os.getenv('PROJECT_ID')
slack_prefix = hashlib.md5(project_id.encode()).hexdigest()
publisher = google.cloud.pubsub_v1.PublisherClient()
db = google.cloud.firestore.Client(project=project_id)


def build_game(game_id):
    return Game(
        game_id=game_id,
        slack_prefix=slack_prefix,
        project_id=project_id,
        publisher=publisher,
        db=db)


def slash_command(request):
    team_id = request.form['team_id']
    channel_id = request.form['channel_id']
    organizer_id = request.form['user_id']
    trigger_id = request.form['trigger_id']
    text = request.form['text']
    slash_datetime_compact = reusable.time.get_now_compact_format()
    game_id = ut.ids.build_game_id(
        slash_datetime_compact, team_id, channel_id, organizer_id, trigger_id)
    logger.info(f'game_id built, game_id={game_id}')
    game = build_game(game_id=game_id)
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
    if resp:
        logger.info(f'exception, game_id={game_id}')
        return resp
    if game.parameter == 'help':
        ut.slack.SlackOperator(game).send_help(organizer_id)
    elif game.parameter == 'freestyle':
        ut.slack.SlackOperator(game).open_setup_freestyle_view(trigger_id)
    elif game.parameter in ('english', 'french'):
        questions = db.collection('qas').document(
            game.parameter).get().to_dict()['content']
        max_number, number, question, answer = ut.qas.select(questions)
        ut.slack.SlackOperator(game).open_setup_automatic_view(
            trigger_id, max_number, number, question, answer)
    logger.info(f'setup_view opened, game_id={game.id}')
    return make_response('', 200)


def message_actions(request):
    message_action = json.loads(request.form['payload'])
    message_action_type = message_action['type']
    user_id = message_action['user']['id']
    if message_action_type not in ('block_actions', 'view_submission'):
        return make_response('', 200)

    if message_action_type == 'view_submission':
        return ma.view_submissions.handle_view_submission(
            user_id, message_action, build_game, slack_prefix)

    if message_action_type == 'block_actions':
        return ma.block_actions.handle_block_action(
            user_id, message_action, build_game, slack_prefix)


def pre_guess_stage(event, context):
    assert context == context

    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_guess_stage_exceptions()
    if resp:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['pre_guess_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game(merge=True)

    slack_operator = ut.slack.SlackOperator(game)
    game.upper_ts, game.lower_ts = slack_operator.post_pre_guess_stage()
    game.nb_members = slack_operator.get_conversation_infos()['num_members']
    max_guessers = min(game.nb_members - 1, game.max_guessers_per_game)
    if game.parameter == 'freestyle':
        max_guessers -= 1
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


def guess_stage(event, context):
    assert context == context
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_guess_stage_exceptions()
    if resp:
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


def pre_vote_stage(event, context):
    assert context == context
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_vote_stage_exceptions()
    if resp:
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


def vote_stage(event, context):
    assert context == context
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(game).handle_vote_stage_exceptions()
    if resp:
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


def pre_result_stage(event, context):
    assert context == context
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_results_stage_exceptions()
    if resp:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['pre_result_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    ut.slack.SlackOperator(game).update_pre_result_stage()

    if len(game.frozen_guessers) >= 1:
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


def result_stage(event, context):
    assert context == context
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_results_stage_exceptions()
    if resp:
        logger.info(f'exception, game_id={game_id}')
        return resp
    game.dict['result_stage_over'] = True
    firestore_editor = ut.firestore.FirestoreEditor(game)
    firestore_editor.set_game(merge=True)
    logger.info(f'sucessfully ended, game_id={game_id}')
    return make_response('', 200)


def freeze(event, context):
    assert event == event and context == context
    teams_ref = db.collection('teams')
    for t in teams_ref.stream():
        team_ref = teams_ref.document(t.id)
        games_ref = team_ref.collection('games')
        for g in games_ref.stream():
            game_id = g.id
            game_dict = g.to_dict()
            if ut.exceptions.game_is_too_old(game_id):
                if 'result_stage_over' in game_dict:
                    ut.firestore.freeze_success(db, game_id, game_dict)
                    kind = 'success'
                else:
                    ut.firestore.freeze_fail(db, game_id, game_dict)
                    kind = 'fail'
                g.reference.delete()
                logger.info(f'{kind} frozen, game_id={g.id}')
    return make_response('', 200)
