import logging
import flask
import slack_sdk.errors
import reusable
import app.utils as ut
import languages
logger = logging.getLogger(__name__)


def game_is_too_old(game_id, max_life_span):
    now = reusable.time.get_now()
    slash_datetime_compact = ut.ids.game_id_to_slash_datetime_compact(game_id)
    slash_datetime = reusable.time.compact_to_datetime(
        slash_datetime_compact)
    delta = ut.time.datetime1_minus_datetime2(
        now, slash_datetime)
    return delta > max_life_span


class ExceptionsHandler:
    def __init__(self, game):
        self.game = game
        self.slack_operator = ut.slack.SlackOperator(self.game)

    @staticmethod
    def game_is_running(game_dict):
        c1 = 'setup_submission' in game_dict
        c2 = 'result_stage_over' not in game_dict
        return c1 and c2

    def get_running_games(self, game_dicts):
        return {gid: game_dicts[gid] for gid in game_dicts if
                self.game_is_running(game_dicts[gid])}

    def get_this_organizer_running_games(self, game_dicts):
        organizer_id = self.game.organizer_id
        running_games = self.get_running_games(game_dicts)
        return {gid: game_dicts[gid] for gid in running_games if
                ut.ids.game_id_to_organizer_id(gid) == organizer_id}

    def count_running_games(self, game_dicts):
        return len(self.get_running_games(game_dicts))

    def count_this_organizer_running_games(self, game_dicts):
        return len(self.get_this_organizer_running_games(game_dicts))

    def max_nb_running_games_reached(self, game_dicts):
        nb_running_games = self.count_running_games(game_dicts)
        return nb_running_games >= self.game.max_running_games

    def max_nb_this_organizer_running_games_reached(self, game_dicts):
        nb_own_running_games = self.count_this_organizer_running_games(
            game_dicts)
        return (nb_own_running_games
                >= self.game.max_running_games_per_organizer)

    def max_nb_these_guessers_reached(self):
        return len(self.game.guessers) >= self.game.max_guessers_per_game

    def no_time_left_to_guess(self):
        return self.game.time_left_to_guess <= 0

    def no_time_left_to_vote(self):
        return self.game.time_left_to_vote <= 0

    def game_is_too_old(self):
        return game_is_too_old(self.game.id, self.game.max_life_span)

    def game_is_dead(self):
        if not self.game.exists:
            logger.info(f'not exist, {self.game.id}')
            return True
        if self.game_is_too_old():
            logger.info(f'too old, {self.game.id}')
            return True
        return False

    def stage_was_recently_trigger(self, last_trigger):
        if last_trigger is None:
            return False
        now = reusable.time.get_now()
        delta = ut.time.datetime1_minus_datetime2(now, last_trigger)
        return delta < self.game.trigger_cooldown

    def guess_stage_was_recently_trigger(self):
        return self.stage_was_recently_trigger(
            self.game.guess_stage_last_trigger)

    def vote_stage_was_recently_trigger(self):
        return self.stage_was_recently_trigger(
            self.game.vote_stage_last_trigger)

    def build_remind_question_truth_msg(self):
        msg = (
            f'Question: {self.game.question}\n\n' 
            f'Answer: {self.game.truth}\n\n')
        return msg

    def build_max_nb_running_games_reached_msg(self, remind):
        msg_template = ('There {} already {} game{} running! '
                        'This is the maximal number allowed.')
        if self.game.max_running_games == 1:
            be = 'is'
            plural = ''
        else:
            be = 'are'
            plural = 's'
        msg = msg_template.format(be, self.game.max_running_games, plural)
        if remind:
            remind_msg = self.build_remind_question_truth_msg()
            msg = remind_msg + msg
        return msg

    def build_max_nb_this_organizer_running_games_reached_msg(
            self, remind):
        msg_template = ('You are already the organizer of {} running game{}. '
                        'This is the maximum number allowed.')
        if self.game.max_running_games_per_organizer == 1:
            plural = ''
        else:
            plural = 's'
        msg = msg_template.format(
            self.game.max_running_games_per_organizer, plural)
        if remind:
            remind_msg = self.build_remind_question_truth_msg()
            msg = remind_msg + msg
        return msg

    def build_game_is_dead_msg(self):
        if self.game_is_dead():
            return 'This game is dead!'

    def build_aborted_cause_recently_triggered_msg(self):
        return f'aborted cause recently triggered, game_id={self.game.id}'

    def build_aborted_cause_already_triggered_msg(self):
        return f'aborted cause already triggered, game_id={self.game.id}'

    def build_slash_command_exception_msg(
            self, in_conversation, game_parameter, game_dicts):
        if not in_conversation:
            return 'Please invite me first to this conversation!'
        p = ['help', 'freestyle'] + languages.LANGUAGES
        if game_parameter not in p:
            return ("Game parameter must be one of "
                    f"{', '.join(p[:-1])} or {p[-1]}.")
        if self.max_nb_this_organizer_running_games_reached(game_dicts):
            m = self.build_max_nb_this_organizer_running_games_reached_msg(
                remind=False)
            return m
        if self.max_nb_running_games_reached(game_dicts):
            m = self.build_max_nb_running_games_reached_msg(
                remind=False)
            return m

    def build_setup_submission_exception_msg(self, game_dicts):
        if self.max_nb_this_organizer_running_games_reached(game_dicts):
            m = self.build_max_nb_this_organizer_running_games_reached_msg(
                remind=True)
            return m
        if self.max_nb_running_games_reached(game_dicts):
            m = self.build_max_nb_running_games_reached_msg(
                remind=True)
            return m

    def build_guess_submission_exception_msg(self, guess):
        if self.no_time_left_to_guess():
            msg = (f'Your guess: {guess}\n\n'
                   'It will not be taken into account '
                   'because the guessing deadline '
                   'has passed!')
            return msg
        if self.max_nb_these_guessers_reached():
            msg = (f'Your guess: {guess}\n\n '
                   'It will not be taken into account '
                   'because there are already '
                   f'{self.game.max_guessers_per_game} guessers. '
                   'This is the maximal number allowed for a game.')
            return msg

    def build_vote_submission_exception_msg(self, vote):
        if self.no_time_left_to_vote():
            msg = (f'Your vote: proposal {vote}.\n\n'
                   'It will not be taken into account '
                   'because the voting deadline has passed!')
            return msg

    @staticmethod
    def build_pick_submission_exception_msg(
            max_number, number_picked_str):
        try:
            number_picked = int(number_picked_str)
        except ValueError:
            return 'Input must be an integer.'
        if number_picked not in range(1, max_number + 1):
            msg = f'{number_picked} is not between 1 and {max_number}.'
            return msg

    def build_guess_click_exception_msg(self, user_id):
        if user_id == self.game.organizer_id and \
                self.game.parameter == 'freestyle':
            return 'As the organizer of this freestyle game, you cannot guess!'
        if user_id in self.game.guessers:
            return 'You have already guessed!'

    def build_vote_click_exception_msg(self, user_id):
        if user_id not in self.game.potential_voters:
            return 'Only guessers can vote!'
        if user_id in self.game.voters:
            return 'You have already voted!'

    def handle_is_dead_exception(self, trigger_id=None, view_id=None):
        if trigger_id is not None:
            assert view_id is None
        if view_id is not None:
            assert trigger_id is None
        exception_msg = self.build_game_is_dead_msg()
        if exception_msg is None:
            return
        if trigger_id is not None:
            self.slack_operator.open_exception_view(trigger_id, exception_msg)
            return flask.make_response('', 200)
        elif view_id is not None:
            self.slack_operator.update_exception_view(view_id, exception_msg)
            return flask.make_response('', 200)
        else:
            return self.slack_operator.build_exception_view_response(
                exception_msg)

    def handle_slash_command_exceptions(self, trigger_id):
        slack_operator = self.slack_operator
        app_user_id = self.slack_operator.get_app_user_id()
        in_conversation = True
        try:
            slack_operator.post_ephemeral(app_user_id, 'I was invited!')
        except slack_sdk.errors.SlackApiError as e:
            assert 'error' in e.response
            if e.response['error'] in ['channel_not_found', 'not_in_channel']:
                in_conversation = False
            else:
                raise e
        game_parameter = self.game.parameter
        game_dicts = self.game.firestore_reader.get_game_dicts()
        exception_msg = self.build_slash_command_exception_msg(
            in_conversation, game_parameter, game_dicts)
        if exception_msg is not None:
            logger.info(
                f'exception slash_command, {exception_msg} {self.game.id}')
            slack_operator.open_exception_view(trigger_id, exception_msg)
            return flask.make_response('', 200)

    def handle_setup_submission_exceptions(self):
        game_dicts = self.game.firestore_reader.get_game_dicts()
        exception_msg = self.build_setup_submission_exception_msg(game_dicts)
        if exception_msg is not None:
            logger.info(
                f'exception setup_submission, {exception_msg} {self.game.id}')
            return self.slack_operator.build_exception_view_response(
                exception_msg)

    def handle_guess_submission_exceptions(self, guess):
        exception_msg = self.build_guess_submission_exception_msg(guess)
        if exception_msg is not None:
            logger.info(
                f'exception guess_submission, {exception_msg} {self.game.id}')
            return self.slack_operator.build_exception_view_response(
                exception_msg)

    def handle_vote_submission_exceptions(self, vote):
        exception_msg = self.build_vote_submission_exception_msg(vote)
        if exception_msg is not None:
            logger.info(
                f'exception vote_submission, {exception_msg} {self.game.id}')
            return self.slack_operator.build_exception_view_response(
                exception_msg)

    def handle_pick_submission_exceptions(
            self, trigger_id, max_number, number_picked_str):
        exception_msg = self.build_pick_submission_exception_msg(
            max_number, number_picked_str)
        if exception_msg is not None:
            logger.info(
                f'exception pick_submission, {exception_msg} {self.game.id}')
            self.slack_operator.push_exception_view(trigger_id, exception_msg)
            return flask.make_response('', 200)

    def handle_guess_click_exceptions(self, user_id, trigger_id):
        exception_msg = self.build_guess_click_exception_msg(user_id)
        if exception_msg is not None:
            logger.info(
                f'exception guess_click, {exception_msg} {self.game.id}')
            self.slack_operator.open_exception_view(trigger_id, exception_msg)
            return flask.make_response('', 200)

    def handle_vote_click_exceptions(self, user_id, trigger_id):
        exception_msg = self.build_vote_click_exception_msg(user_id)
        if exception_msg is not None:
            logger.info(
                f'exception vote_click, {exception_msg} {self.game.id}')
            self.slack_operator.open_exception_view(trigger_id, exception_msg)
            return flask.make_response('', 200)

    def handle_pre_guess_stage_exceptions(self):
        if self.game.pre_guess_stage_already_triggered:
            logger.info(
                self.build_aborted_cause_already_triggered_msg())
            return flask.make_response('', 200)

    def handle_guess_stage_exceptions(self):
        if self.guess_stage_was_recently_trigger():
            logger.info(
                self.build_aborted_cause_recently_triggered_msg())
            return flask.make_response('', 200)

    def handle_pre_vote_stage_exceptions(self):
        if self.game.pre_vote_stage_already_triggered:
            logger.info(
                self.build_aborted_cause_already_triggered_msg())
            return flask.make_response('', 200)

    def handle_vote_stage_exceptions(self):
        if self.vote_stage_was_recently_trigger():
            logger.info(
                self.build_aborted_cause_recently_triggered_msg())
            return flask.make_response('', 200)

    def handle_pre_results_stage_exceptions(self):
        if self.game.pre_result_stage_already_triggered:
            logger.info(
                self.build_aborted_cause_already_triggered_msg())
            return flask.make_response('', 200)

    def handle_results_stage_exceptions(self):
        if self.game.result_stage_over:
            logger.info(
                f'exception, results_stage over {self.game.id}')
            return flask.make_response('', 200)
