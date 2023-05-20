import json
import logging
import time
import flask
import tools
import app.utils as ut
logger = logging.getLogger(__name__)


def no_crash(f):
    def decored(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(e, stack_info=True)
    return decored


def multi_tries(f):
    def decored(*args, **kwargs):
        for duration in [10, 30, 60]:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.warning(e, stack_info=True)
                logger.warning(f'sleeping {duration} seconds before next try')
                time.sleep(duration)
        return f(*args, **kwargs)
    return decored


def verify_signature(slack_verifier, body, headers):
    if not slack_verifier.is_valid_request(body, headers):
        flask.abort(401)


def auth_test(slack_client):
    return tools.slack_api.auth_test(slack_client)


def post_message(slack_client, channel_id, blocks, alternative_text):
    return tools.slack_api.chat_postmessage(
        slack_client, channel_id, blocks, alternative_text)


def post_ephemeral(slack_client, channel_id, user_id, msg):
    tools.slack_api.chat_postephemeral(
        slack_client, channel_id, user_id, msg)


def update_message(slack_client, channel_id, blocks, ts, alternative_text):
    tools.slack_api.chat_update(
        slack_client, channel_id, blocks, ts, alternative_text)


def open_view(slack_client, trigger_id, view):
    tools.slack_api.views_open(slack_client, trigger_id, view)


def update_view(slack_client, view_id, view):
    tools.slack_api.views_update(slack_client, view_id, view)


def push_view(slack_client, trigger_id, view):
    tools.slack_api.views_push(slack_client, trigger_id, view)


def build_view_response(view):
    res = {'response_action': 'update', 'view': view}
    res = flask.Response(
        json.dumps(res),
        mimetype='application/json',
        status=200)
    return res


def open_exception_view(slack_client, language, trigger_id, msg):
    exception_view = ut.views.build_exception_view(language, msg)
    open_view(slack_client, trigger_id, exception_view)


def update_exception_view(slack_client, language, view_id, msg):
    exception_view = ut.views.build_exception_view(language, msg)
    update_view(slack_client, view_id, exception_view)


def push_exception_view(slack_client, language, trigger_id, msg):
    exception_view = ut.views.build_exception_view(language, msg)
    push_view(slack_client, trigger_id, exception_view)


def build_exception_view_response(language, msg):
    exception_view = ut.views.build_exception_view(language, msg)
    return build_view_response(exception_view)


class SlackOperator:
    def __init__(self, game):
        self.game = game
        self.language = self.game.language
        self.slack_client = self.game.slack_client
        self.block_builder = ut.blocks.BlockBuilder(game)
        self.view_builder = ut.views.ViewBuilder(game)
        self.tagging = self.game.exists and self.game.tagging
        self.multi_tries_post_message = multi_tries(self.post_message)
        self.multi_tries_update_upper = multi_tries(self.update_upper)
        self.multi_tries_update_lower = multi_tries(self.update_lower)
        self.no_crash_post_ephemeral = no_crash(self.post_ephemeral)
        self.no_crash_update_upper = no_crash(self.update_upper)
        self.no_crash_update_lower = no_crash(self.update_lower)
        self.organizer_display = ut.users.user_display(self.game.organizer_id)

    def add_tag_to_text(self, text):
        if self.tagging:
            text = ut.tag.add_tag_to_text(text, self.game.tag)
        return text

    def add_tag_to_blocks(self, blocks):
        if self.tagging:
            blocks = ut.tag.add_tag_to_json_list(blocks, self.game.tag)
        return blocks

    def add_tag_to_view(self, view):
        if self.tagging:
            view = ut.tag.add_tag_to_json(view, self.game.tag)
        return view

    def get_app_user_id(self):
        return auth_test(self.slack_client)['user_id']

    def post_message(self, blocks):
        blocks = self.add_tag_to_blocks(blocks)
        return post_message(
            self.slack_client, self.game.channel_id, blocks,
            ut.text.New_message[self.language])

    def post_ephemeral(self, user_id, msg):
        msg = self.add_tag_to_text(msg)
        post_ephemeral(
            self.slack_client, self.game.channel_id, user_id, msg)

    def update_message(self, blocks, ts):
        blocks = self.add_tag_to_blocks(blocks)
        update_message(
            self.slack_client, self.game.channel_id, blocks, ts,
            ut.text.Message_updated[self.language])

    def open_view(self, trigger_id, view):
        view = self.add_tag_to_view(view)
        open_view(self.slack_client, trigger_id, view)

    def update_view(self, view_id, view):
        view = self.add_tag_to_view(view)
        update_view(self.slack_client, view_id, view)

    def push_view(self, trigger_id, view):
        view = self.add_tag_to_view(view)
        push_view(self.slack_client, trigger_id, view)

    def open_exception_view(self, trigger_id, msg):
        msg = self.add_tag_to_text(msg)
        open_exception_view(self.slack_client, self.language, trigger_id, msg)

    def update_exception_view(self, view_id, msg):
        msg = self.add_tag_to_text(msg)
        update_exception_view(self.slack_client, self.language, view_id, msg)

    def push_exception_view(self, trigger_id, msg):
        msg = self.add_tag_to_text(msg)
        push_exception_view(self.slack_client, self.language, trigger_id, msg)

    def build_exception_view_response(self, msg):
        msg = self.add_tag_to_text(msg)
        return build_exception_view_response(self.language, msg)

    def update_upper(self, blocks):
        self.update_message(blocks, self.game.upper_ts)

    def update_lower(self, blocks):
        self.update_message(blocks, self.game.lower_ts)

    def open_setup_freestyle_view(self, trigger_id):
        view = self.view_builder.build_setup_freestyle_view()
        self.open_view(trigger_id, view)

    def open_setup_automatic_view(
            self, trigger_id, url, max_number, number, question, answer):
        view = self.view_builder.build_setup_automatic_view(
            url, max_number, number, question, answer)
        self.open_view(trigger_id, view)

    def update_setup_automatic_view(
            self, view_id, url, max_number, number, question, answer):
        view = self.view_builder.build_setup_automatic_view(
            url, max_number, number, question, answer)
        self.update_view(view_id, view)

    def open_guess_view(self, trigger_id):
        self.open_view(trigger_id, self.view_builder.build_guess_view())

    def open_vote_view(self, trigger_id, voter):
        view = self.view_builder.build_vote_view(voter)
        self.open_view(trigger_id, view)

    def send_help(self, user_id):
        msg = ut.help.build_msg(self.game)
        self.post_ephemeral(user_id, msg)

    def send_vote_reminders(self):
        for u in self.game.potential_voters:
            user_display = ut.users.user_display(u)
            msg = ut.text.you_can_now_vote[self.language].format(
                user_display=user_display,
                organizer_display=self.organizer_display)
            self.no_crash_post_ephemeral(u, msg)

    def send_is_over_notifications(self):
        for u in self.game.frozen_guessers:
            msg = ut.text.game_is_over[self.language].format(
                organizer_display=self.organizer_display)
            self.no_crash_post_ephemeral(u, msg)

    def post_pre_guess_stage_upper(self):
        return self.multi_tries_post_message(
            self.block_builder.build_pre_guess_stage_upper_blocks())

    def post_pre_guess_stage_lower(self):
        return self.multi_tries_post_message(
            self.block_builder.build_pre_guess_stage_lower_blocks())

    def update_pre_vote_stage_upper(self):
        self.no_crash_update_upper(
            self.block_builder.build_pre_vote_stage_upper_blocks())

    def update_pre_vote_stage_lower(self):
        self.no_crash_update_lower(
            self.block_builder.build_pre_vote_stage_lower_blocks())

    def update_pre_result_stage_upper(self):
        self.no_crash_update_upper(
            self.block_builder.build_pre_result_stage_upper_blocks())

    def update_pre_result_stage_lower(self):
        self.no_crash_update_lower(
            self.block_builder.build_pre_result_stage_lower_blocks())

    def update_guess_stage_upper(self):
        self.multi_tries_update_upper(
            self.block_builder.build_guess_stage_upper_blocks())

    def update_guess_stage_lower(self):
        self.no_crash_update_lower(
            self.block_builder.build_guess_stage_lower_blocks())

    def update_vote_stage_upper(self):
        self.multi_tries_update_upper(
            self.block_builder.build_vote_stage_upper_blocks())

    def update_vote_stage_lower(self):
        self.no_crash_update_lower(
            self.block_builder.build_vote_stage_lower_blocks())

    def update_result_stage_upper(self):
        self.multi_tries_update_upper(
            self.block_builder.build_result_stage_upper_blocks())

    def update_result_stage_lower(self):
        self.multi_tries_update_lower(
            self.block_builder.build_result_stage_lower_blocks())

    def post_pre_guess_stage(self):
        return self.post_pre_guess_stage_upper(), \
               self.post_pre_guess_stage_lower()

    def update_pre_vote_stage(self):
        self.update_pre_vote_stage_upper()
        self.update_pre_vote_stage_lower()

    def update_pre_result_stage(self):
        self.update_pre_result_stage_upper()
        self.update_pre_result_stage_lower()

    def update_guess_stage(self):
        self.update_guess_stage_upper()
        self.update_guess_stage_lower()

    def update_vote_stage(self):
        self.update_vote_stage_upper()
        self.update_vote_stage_lower()

    def update_result_stage(self):
        self.update_result_stage_upper()
        self.update_result_stage_lower()
