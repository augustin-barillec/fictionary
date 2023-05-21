import argparse
import copy
import datetime
import hashlib
import json
import os
import time
import flask
import google.cloud.bigquery
import google.cloud.pubsub_v1
import google.cloud.firestore
import slack_sdk.signature
import reusable
import app.utils as ut
import app.interactivity
import app.game
import version
logger = reusable.root_logger.configure_root_logger()
context = argparse.Namespace()
context.publisher = google.cloud.pubsub_v1.PublisherClient()
context.project_id = os.environ['PROJECT_ID']
context.db = google.cloud.firestore.Client(project=context.project_id)
context.surface_prefix = hashlib.md5(context.project_id.encode()).hexdigest()


def verify_signature(body, headers):
    slack_signing_secret = ut.firestore.get_slack_signing_secret(
        context.db)
    slack_verifier = slack_sdk.signature.SignatureVerifier(
        slack_signing_secret)
    ut.slack.verify_signature(slack_verifier, body, headers)


def build_game(game_id):
    return app.game.Game(
        db=context.db,
        publisher=context.publisher,
        surface_prefix=context.surface_prefix,
        project_id=context.project_id,
        game_id=game_id)


context.build_game_func = build_game


def slash_command(request):
    """This HTTP Cloud Function is triggered when a user sends the slash
    command "/fictionary" followed by one the three following parameters:
    "help", "freestyle", "automatic".

    With the last two parameters, a game is stored in Firestore with
    the following attributes: version, parameter and tag. The tag is used
    during the Cypress tests for tagging messages. Thus, they can be
    identified during the tests.

    "/fictionary help" displays an ephemeral message which gives information
    about this app.

    "/fictionary freestyle" opens a game setup view where the user has to
    come up with the question and the answer.

    "/fictionary automatic" opens a game setup view where the user can pick
    a question from a question bank.
    """
    body = request.get_data()
    headers = request.headers
    verify_signature(body, headers)
    form = request.form
    team_id = form['team_id']
    channel_id = form['channel_id']
    organizer_id = form['user_id']
    trigger_id = form['trigger_id']
    text = form['text']
    slash_datetime_compact = reusable.time.get_now_compact_format()
    game_id = ut.ids.build_game_id(
        slash_datetime_compact, team_id, channel_id, organizer_id, trigger_id)
    game = build_game(game_id)
    logger.info(f'game built, game_id={game_id}')
    game.version = version.VERSION
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
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_slash_command_exceptions(trigger_id)
    if resp is not None:
        return resp
    elif game.parameter == 'help':
        ut.slack.SlackOperator(game).send_help(organizer_id)
        return flask.make_response('', 200)
    ut.firestore.FirestoreEditor(game).set_game()
    logger.info(f'game stored, game_id={game_id}')
    if game.parameter == 'freestyle':
        ut.slack.SlackOperator(game).open_setup_freestyle_view(trigger_id)
    elif game.parameter == 'automatic':
        url = ut.questions.get_questions_url(game)
        questions, answers = ut.questions.get_questions_answers(game)
        max_number = len(questions)
        number, question, answer = ut.questions.select(questions, answers)
        ut.slack.SlackOperator(game).open_setup_automatic_view(
            trigger_id, url, max_number, number, question, answer)
    logger.info(f'setup_view opened, game_id={game.id}')
    return flask.make_response('', 200)


def interactivity(request):
    """This HTTP function is triggered any time a user interacts with an
    object of a game: game setup view configuration and submission,
    guess button click and guess view submission, vote button click and
    vote view submission.
    """
    body = request.get_data()
    headers = request.headers
    verify_signature(body, headers)
    payload = json.loads(request.form['payload'])
    payload_type = payload['type']
    if payload_type == 'view_submission':
        return app.interactivity.view_submissions.handle_view_submission(
            context, payload)
    elif payload_type == 'block_actions':
        return app.interactivity.block_actions.handle_block_action(
            context, payload)
    return flask.make_response('', 200)


def pre_guess_stage(event, context_):
    """This event-driven function is triggered by the interactivity function
    when a game setup view is submitted. It displays two messages: the upper
    message and the lower message.

    These two messages are updated through the whole game. The upper message is
    updated only when the game changes of stage. The upper message will contain
    the guess button and the click button. The lower messages is updated
    frequently (every 4 seconds). It contains the timer and the names of the
    users guessing or voting. With only one message, the buttons would have
    been also refreshed every 4 seconds which is inconvenient for the users.

    This function stores the timestamps of the publication of these two
    messages in Firestore so that they can be updated later.

    This function computes also the starting time and the deadline for guessing
    and stores it in Firestore.

    Finally, it triggers the guess stage function.
    """
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_guess_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['pre_guess_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game()

    slack_operator = ut.slack.SlackOperator(game)
    resp_upper, resp_lower = slack_operator.post_pre_guess_stage()
    game.upper_ts = resp_upper['ts']
    game.lower_ts = resp_lower['ts']
    game.guessers = dict()
    game.guess_start = reusable.time.get_now()
    game.guess_deadline = ut.time.compute_deadline(
        game.guess_start, game.time_to_guess)
    for attribute in [
        'upper_ts',
        'lower_ts',
        'guessers',
        'guess_start',
        'guess_deadline'
    ]:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game()

    game = build_game(game_id)
    ut.slack.SlackOperator(game).update_guess_stage()
    game.stage_triggerer.trigger_guess_stage()
    logger.info(f'guess_stage triggered, game_id={game_id}')
    return flask.make_response('', 200)


def guess_stage(event, context_):
    """This event-driven function is triggered by the pre_guess_stage function.
    This function refreshes the lower message containing the guessing timer and
    the names of the guessers. It triggers the pre_vote_stage function where
    there is no more time to guess or when the maximal number of players is
    reached.
    """
    assert context_ == context_
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_guess_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['guess_stage_last_trigger'] = call_datetime
    ut.firestore.FirestoreEditor(game).set_game()
    while True:
        game = build_game(game_id)
        ut.slack.SlackOperator(game).update_guess_stage_lower()
        c1 = game.time_left_to_guess <= 0
        c2 = game.nb_remaining_potential_guessers <= 0
        if c1 or c2:
            game.dict['frozen_guessers'] = copy.deepcopy(game.dict['guessers'])
            game.dict['guess_stage_over'] = True
            ut.firestore.FirestoreEditor(game).set_game()
            game.stage_triggerer.trigger_pre_vote_stage()
            logger.info(f'pre_vote_stage triggered, game_id={game_id}')
            return flask.make_response('', 200)
        if ut.time.datetime1_minus_datetime2(
                reusable.time.get_now(), call_datetime) > \
                game.self_trigger_threshold:
            game.stage_triggerer.trigger_guess_stage()
            logger.info(f'guess_stage self-triggered, game_id={game_id}')
            return flask.make_response('', 200)
        time.sleep(game.refresh_interval)


def pre_vote_stage(event, context_):
    """This event-driven function is triggered by the vote_stage function.
    It shuffles all the guesses, computes the voting start time and deadline.
    It then displays the shuffled messages in Slack and triggers the
    vote_stage function.
    """
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_vote_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['pre_vote_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game()
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
    ut.firestore.FirestoreEditor(game).set_game()

    game = build_game(game_id)
    slack_operator = ut.slack.SlackOperator(game)
    slack_operator.update_vote_stage()
    slack_operator.send_vote_reminders()
    game.stage_triggerer.trigger_vote_stage()
    logger.info(f'vote_stage triggered, game_id={game_id}')
    return flask.make_response('', 200)


def vote_stage(event, context_):
    """This event-driven function is triggered by the pre_vote_stage function.
    This function refreshes the lower message containing the voting timer and
    the names of the voters. It triggers the pre_result_stage function when
    there is no more time to vote or when the maximal number of voters is
    reached.
    """
    assert context_ == context_
    call_datetime = reusable.time.get_now()
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(game).handle_vote_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['vote_stage_last_trigger'] = call_datetime
    ut.firestore.FirestoreEditor(game).set_game()
    while True:
        game = build_game(game_id)
        ut.slack.SlackOperator(game).update_vote_stage_lower()
        c1 = len(game.frozen_guessers) == 1
        c2 = game.time_left_to_vote <= 0
        c3 = not game.remaining_potential_voters
        if c1 or c2 or c3:
            game.dict['frozen_voters'] = copy.deepcopy(game.dict['voters'])
            game.dict['vote_stage_over'] = True
            ut.firestore.FirestoreEditor(game).set_game()
            game.stage_triggerer.trigger_pre_result_stage()
            logger.info(f'pre_result_stage triggered, game_id={game_id}')
            return flask.make_response('', 200)
        if ut.time.datetime1_minus_datetime2(
                reusable.time.get_now(),
                call_datetime) > game.self_trigger_threshold:
            game.stage_triggerer.trigger_vote_stage()
            logger.info(f'vote_stage self-triggered, game_id={game_id}')
            return flask.make_response('', 200)
        time.sleep(game.refresh_interval)


def pre_result_stage(event, context_):
    """This event-driven function is triggered by the vote_stage function.
    It computes the results of the game which contain the scores, the voting
    graph and the winners for that game. It then displays this information
    in Slack and triggers the result_stage function.
    """
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_pre_results_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['pre_result_stage_already_triggered'] = True
    ut.firestore.FirestoreEditor(game).set_game()
    ut.slack.SlackOperator(game).update_pre_result_stage()

    game.results = ut.results.ResultsBuilder(game).build_results()
    game.max_score = ut.results.compute_max_score(game)
    game.winners = ut.results.compute_winners(game)
    for attribute in ['results', 'max_score', 'winners']:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game()

    slack_operator = ut.slack.SlackOperator(game)
    slack_operator.update_result_stage()
    slack_operator.send_is_over_notifications()
    game.stage_triggerer.trigger_result_stage()
    logger.info(f'result_stage triggered, game_id={game_id}')
    return flask.make_response('', 200)


def result_stage(event, context_):
    """This event-driven function is triggered by the pre_result_stage
    function. It essentially only reports in Firestore that the game ended
    successfully.
    """
    assert context_ == context_
    game_id = event['attributes']['game_id']
    logger.info(f'start, game_id={game_id}')
    game = build_game(game_id)
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_results_stage_exceptions()
    if resp is not None:
        return resp
    game.dict['result_stage_over'] = True
    firestore_editor = ut.firestore.FirestoreEditor(game)
    firestore_editor.set_game()
    logger.info(f'successfully ended, game_id={game_id}')
    return flask.make_response('', 200)


def clean(event, context_):
    """This event-driven function is designed to be triggered periodically.
    In production, it is triggered once per day.

    An old game is a game that started more than one hour ago. This function
    deletes old games that ended successfully and report data about them in
    BigQuery (but not data written by users).

    This function moves old games that failed (meaning they do not contain in
    Firestore the entry 'result_stage_over') in the fails collection to help
    for debugging. These failed games are automatically deleted about 3 days
    after they were moved.
    """
    assert event == event and context_ == context_
    bq_client = google.cloud.bigquery.Client(project=context.project_id)
    game_ids = []
    game_dicts = []
    outcomes = []
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
                    outcome = 'success'
                elif sorted(game_dict.keys()) == [
                        'parameter', 'tag', 'version']:
                    outcome = 'unsubmitted'
                else:
                    fail_ref = context.db.collection('fails').document(game_id)
                    expire_at = \
                        reusable.time.get_now() + datetime.timedelta(days=3)
                    game_dict['expire_at'] = expire_at
                    fail_ref.set(game_dict, merge=False)
                    outcome = 'fail'
                g.reference.delete()
                logger.info(f'{outcome}, game_id={g.id}')
                game_ids.append(game_id)
                game_dicts.append(game_dict)
                outcomes.append(outcome)
    monitoring = ut.monitoring.compute_monitoring(
        game_ids, game_dicts, outcomes)
    ut.monitoring.upload_monitoring(
        bq_client, context.project_id, monitoring)
    logger.info(f'monitoring uploaded: {len(monitoring)} lines')
    return flask.make_response('', 200)
