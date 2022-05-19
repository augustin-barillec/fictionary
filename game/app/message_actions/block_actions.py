import logging
from flask import make_response
from app import utils as ut

logger = logging.getLogger(__name__)


def handle_block_action(
        user_id, message_action, build_game_func, slack_prefix):
    trigger_id = message_action['trigger_id']
    action_block_id = message_action['actions'][0]['block_id']
    if not action_block_id.startswith(slack_prefix):
        return make_response('', 200)
    game_id = ut.ids.slack_object_id_to_game_id(action_block_id)
    game = build_game_func(game_id)
    slack_operator = ut.slack.SlackOperator(game)
    eh = ut.exceptions.ExceptionsHandler(game)
    resp = eh.handle_is_dead_exception(trigger_id)
    if resp:
        return resp

    c1 = action_block_id.startswith(slack_prefix + '#pick_block')
    c2 = action_block_id.startswith(slack_prefix + '#shuffle_block')

    qa = None
    if c1 or c2:
        qa = game.db.collection('qas').document(
            game.parameter).get().to_dict()['content']

    if c1:
        return handle_pick(
            qa, message_action, game, slack_operator, eh)

    if c2:
        return handle_shuffle(
            qa, message_action, game, slack_operator, eh)

    if action_block_id.startswith(slack_prefix + '#guess_button_block'):
        return handle_guess_click(
            user_id, trigger_id, game, slack_operator, eh)

    if action_block_id.startswith(slack_prefix + '#vote_button_block'):
        return handle_vote_click(
            user_id, trigger_id, game, slack_operator, eh)


def handle_pick(qa, message_action, game, slack_operator, eh):
    view_id = message_action['view']['id']
    number_picked = int(message_action['actions'][0]['value'])
    max_number, number, question, answer = ut.qas.select(
        qa, number_picked)
    slack_operator.update_setup_automatic_view(
        view_id, max_number, number, question, answer)
    logger.info('pick')
    return make_response('', 200)


def handle_shuffle(
        qa, message_action, game, slack_operator, eh):
    view_id = message_action['view']['id']
    max_number, number, question, answer = ut.qas.select(qa)
    slack_operator.update_setup_automatic_view(
        view_id, max_number, number, question, answer)
    logger.info(f'shuffle, user_id={user_id}, game_id={game.id}')
    return make_response('', 200)


def handle_guess_click(
        user_id, trigger_id, game, slack_operator, exceptions_handler):
    resp = exceptions_handler.handle_guess_click_exceptions(
        user_id, trigger_id)
    if resp:
        return resp
    slack_operator.open_guess_view(trigger_id)
    logger.info(f'guess_view opened, user_id={user_id}, game_id={game.id}')
    return make_response('', 200)


def handle_vote_click(
        user_id, trigger_id, game, slack_operator, exceptions_handler):
    resp = exceptions_handler.handle_vote_click_exceptions(user_id, trigger_id)
    if resp:
        return resp
    slack_operator.open_vote_view(trigger_id, user_id)
    logger.info(f'vote_view opened, user_id={user_id}, game_id={game.id}')
    return make_response('', 200)
