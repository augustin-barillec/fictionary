import logging
import flask
import app.utils as ut
logger = logging.getLogger(__name__)


class BlockActionHandler:
    def __init__(self, context, payload):
        self.context = context
        self.payload = payload
        assert self.payload['type'] == 'block_actions'
        self.user_id = self.payload['user']['id']
        self.trigger_id = self.payload['trigger_id']
        self.action_block_id = self.payload['actions'][0]['block_id']
        assert self.action_block_id.startswith(context.surface_prefix)
        self.game_id = ut.ids.surface_id_to_game_id(self.action_block_id)
        self.game = context.build_game_func(self.game_id)
        self.slack_operator = ut.slack.SlackOperator(self.game)
        self.exceptions_handler = ut.exceptions.ExceptionsHandler(self.game)

    @property
    def view_id(self):
        return self.payload['view']['id']

    def handle_pick_submission(self):
        number_picked_str = self.payload['actions'][0]['value']
        url = ut.questions.get_questions_url(self.game)
        questions, answers = ut.questions.get_questions_answers(self.game)
        max_number = len(questions)
        resp = self.exceptions_handler.handle_pick_submission_exceptions(
            self.trigger_id, max_number, number_picked_str)
        if resp is not None:
            return resp
        number_picked = int(number_picked_str)
        number, question, answer = ut.questions.select(
            questions, answers, number_picked)
        assert number_picked == number
        self.slack_operator.update_setup_automatic_view(
            self.view_id, url, max_number, number_picked, question, answer)
        logger.info(f'question {number_picked} picked, '
                    f'user_id={self.user_id}, game_id={self.game.id}')
        return flask.make_response('', 200)

    def handle_shuffle_click(self):
        url = ut.questions.get_questions_url(self.game)
        questions, answers = ut.questions.get_questions_answers(self.game)
        max_number = len(questions)
        number_random, question, answer = ut.questions.select(
            questions, answers)
        self.slack_operator.update_setup_automatic_view(
            self.view_id, url, max_number, number_random, question, answer)
        logger.info(f'question {number_random} shuffled, '
                    f'user_id={self.user_id}, game_id={self.game.id}')
        return flask.make_response('', 200)

    def handle_guess_click(self):
        resp = self.exceptions_handler.handle_guess_click_exceptions(
            self.user_id, self.trigger_id)
        if resp is not None:
            return resp
        self.slack_operator.open_guess_view(self.trigger_id)
        logger.info(f'guess_view opened, user_id={self.user_id}, '
                    f'game_id={self.game.id}')
        return flask.make_response('', 200)

    def handle_vote_click(self):
        resp = self.exceptions_handler.handle_vote_click_exceptions(
            self.user_id, self.trigger_id)
        if resp is not None:
            return resp
        self.slack_operator.open_vote_view(self.trigger_id, self.user_id)
        logger.info(f'vote_view opened, user_id={self.user_id}, '
                    f'game_id={self.game.id}')
        return flask.make_response('', 200)

    def handle(self):
        c1 = self.action_block_id.startswith(
                self.context.surface_prefix + '#pick_block')
        c2 = self.action_block_id.startswith(
                self.context.surface_prefix + '#shuffle_block')
        c3 = self.action_block_id.startswith(
                self.context.surface_prefix + '#guess_button_block')
        c4 = self.action_block_id.startswith(
                self.context.surface_prefix + '#vote_button_block')
        resp = None
        if c1 or c2:
            resp = self.exceptions_handler.handle_is_dead_exception(
                view_id=self.view_id)
        elif c3 or c4:
            resp = self.exceptions_handler.handle_is_dead_exception(
                trigger_id=self.trigger_id)
        if resp is not None:
            return resp
        if c1:
            return self.handle_pick_submission()
        if c2:
            return self.handle_shuffle_click()
        if c3:
            return self.handle_guess_click()
        if c4:
            return self.handle_vote_click()


def handle_block_action(context, payload):
    if not payload['actions'][0]['block_id'].startswith(
            context.surface_prefix):
        return flask.make_response('', 200)
    return BlockActionHandler(context, payload).handle()
