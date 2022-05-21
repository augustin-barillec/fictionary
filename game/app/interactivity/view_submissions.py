import logging
import reusable
from flask import make_response
from app import utils as ut

logger = logging.getLogger(__name__)


class ViewSubmissionHandler:

    def __init__(self, payload, context):
        self.payload = payload
        self.context = context
        assert self.payload['type'] == 'view_submission'
        self.user_id = self.payload['user']['id']
        self.view = self.payload['view']
        self.view_callback_id = self.view['callback_id']
        assert self.view_callback_id.startswith(context.surface_prefix)
        self.game_id = ut.ids.surface_id_to_game_id(self.view_callback_id)
        self.game = context.build_game_func(self.game_id)
        self.exceptions_handler = ut.exceptions.ExceptionsHandler(self.game)

    def finalize_setup_submission(self, question, truth):
        self.game.setup_submission = reusable.time.get_now()
        self.game.question = question
        self.game.truth = truth
        resp = self.exceptions_handler.handle_setup_submission_exceptions()
        if resp is not None:
            return resp
        self.game.dict = dict()
        for attribute in [
            'setup_submission',
            'question',
            'truth'
        ]:
            self.game.dict[attribute] = self.game.__dict__[attribute]
        ut.firestore.FirestoreEditor(self.game).set_game(merge=True)
        self.game.stage_triggerer.trigger_pre_guess_stage()
        logger.info(f'pre_guess_stage triggered, game_id={self.game.id}')
        return make_response('', 200)

    def handle_setup_freestyle_submission(self):
        question, truth = ut.views.collect_setup_freestyle(self.view)
        return self.finalize_setup_submission(question, truth)

    def handle_setup_automatic_submission(self):
        question, truth = ut.views.collect_setup_automatic(self.view)
        return self.finalize_setup_submission(question, truth)

    def handle_guess_submission(self):
        guess = ut.views.collect_guess(self.view)
        resp = self.exceptions_handler.handle_guess_submission_exceptions(
            guess)
        if resp is not None:
            return resp
        guess_ts = reusable.time.get_now()
        self.game.dict['guessers'][self.user_id] = [guess_ts, guess]
        ut.firestore.FirestoreEditor(self.game).set_game(merge=True)
        logger.info(f'guess recorded, guesser_id={self.user_id}, '
                    f'game_id={self.game.id}')
        return make_response('', 200)

    def handle_vote_submission(self):
        vote = ut.views.collect_vote(self.view)
        resp = self.exceptions_handler.handle_vote_submission_exceptions(vote)
        if resp is not None:
            return resp
        vote_ts = reusable.time.get_now()
        self.game.dict['voters'][self.user_id] = [vote_ts, vote]
        ut.firestore.FirestoreEditor(self.game).set_game(merge=True)
        logger.info(f'vote recorded, voter_id={self.user_id}, '
                    f'game_id={self.game.id} ')
        return make_response('', 200)


def handle_view_submission(payload, context):
    if not payload['view']['callback_id'].startswith(context.surface_prefix):
        return make_response('', 200)
    view_submission_handler = ViewSubmissionHandler(payload, context)
    resp = view_submission_handler.\
        exceptions_handler.handle_is_dead_exception()
    if resp is not None:
        return resp
    if view_submission_handler.view_callback_id.startswith(
            context.surface_prefix + '#setup_freestyle_view'):
        return view_submission_handler.handle_setup_freestyle_submission()
    if view_submission_handler.view_callback_id.startswith(
            context.surface_prefix + '#setup_automatic_view'):
        return view_submission_handler.handle_setup_automatic_submission()
    if view_submission_handler.view_callback_id.startswith(
            context.surface_prefix + '#guess_view'):
        return view_submission_handler.handle_guess_submission()
    if view_submission_handler.view_callback_id.startswith(
            context.surface_prefix + '#vote_view'):
        return view_submission_handler.handle_vote_submission()
