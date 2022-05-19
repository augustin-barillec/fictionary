import logging
import reusable
from flask import make_response
from app import utils as ut

logger = logging.getLogger(__name__)


def handle_view_submission(
        user_id, message_action, build_game_func, slack_prefix):
    view = message_action['view']
    view_callback_id = view['callback_id']
    if not view_callback_id.startswith(slack_prefix):
        return make_response('', 200)

    game_id = ut.ids.slack_object_id_to_game_id(view_callback_id)
    game = build_game_func(game_id)

    eh = ut.exceptions.ExceptionsHandler(game)
    resp = eh.handle_is_dead_exception()
    if resp:
        return resp

    if view_callback_id.startswith(slack_prefix + '#setup_freestyle_view'):
        return handle_setup_freestyle_submission(game, view)

    if view_callback_id.startswith(slack_prefix + '#setup_automatic_view'):
        return handle_setup_automatic_submission(game, view)

    if view_callback_id.startswith(slack_prefix + '#guess_view'):
        return handle_guess_submission(user_id, game, view, eh)

    if view_callback_id.startswith(slack_prefix + '#vote_view'):
        return handle_vote_submission(user_id, game, view, eh)


def handle_setup_freestyle_submission(game, setup_freestyle_view):
    question, truth = ut.views.collect_setup_freestyle(
        setup_freestyle_view)
    game.setup_submission = reusable.time.get_now()
    game.question = question
    game.truth = truth
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_setup_submission_exceptions()
    if resp:
        return resp

    game.dict = dict()
    for attribute in [
        'setup_submission',
        'question',
        'truth',
    ]:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    game.stage_triggerer.trigger_pre_guess_stage()
    logger.info(f'pre_guess_stage triggered, game_id={game.id}')
    return make_response('', 200)


def handle_setup_automatic_submission(game, setup_automatic_view):
    question, truth = ut.views.collect_setup_automatic(setup_automatic_view)
    game.setup_submission = reusable.time.get_now()
    game.question = question
    game.truth = truth
    resp = ut.exceptions.ExceptionsHandler(
        game).handle_setup_submission_exceptions()
    if resp:
        return resp

    game.dict = dict()
    for attribute in [
        'setup_submission',
        'question',
        'truth'
    ]:
        game.dict[attribute] = game.__dict__[attribute]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    game.stage_triggerer.trigger_pre_guess_stage()
    logger.info(f'pre_guess_stage triggered, game_id={game.id}')
    return make_response('', 200)


def handle_guess_submission(
        user_id, game, guess_view, exceptions_handler):
    guess = ut.views.collect_guess(guess_view)
    resp = exceptions_handler.handle_guess_submission_exceptions(guess)
    if resp:
        return resp
    guess_ts = reusable.time.get_now()
    game.dict['guessers'][user_id] = [guess_ts, guess]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    logger.info(f'guess recorded, guesser_id={user_id}, game_id={game.id}')
    return make_response('', 200)


def handle_vote_submission(
        user_id, game, vote_view, exceptions_handler):
    vote = ut.views.collect_vote(vote_view)
    resp = exceptions_handler.handle_vote_submission_exceptions(vote)
    if resp:
        return resp
    vote_ts = reusable.time.get_now()
    game.dict['voters'][user_id] = [vote_ts, vote]
    ut.firestore.FirestoreEditor(game).set_game(merge=True)
    logger.info(f'vote recorded, voter_id={user_id}, game_id={game.id} ')
    return make_response('', 200)
