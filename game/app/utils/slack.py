import json
import reusable
from flask import Response
from app.utils import blocks, help, tag, users, views


def auth_test(slack_client):
    return reusable.slack_api.auth_test(slack_client)


def post_message(slack_client, channel_id, blocks_):
    return reusable.slack_api.chat_postmessage(
        slack_client, channel_id, blocks_)


def post_ephemeral(slack_client, channel_id, user_id, msg):
    reusable.slack_api.chat_postephemeral(
        slack_client, channel_id, user_id, msg)


def update_message(slack_client, channel_id, blocks_, ts):
    reusable.slack_api.chat_update(slack_client, channel_id, blocks_, ts)


def open_view(slack_client, trigger_id, view):
    reusable.slack_api.views_open(slack_client, trigger_id, view)


def update_view(slack_client, view_id, view):
    reusable.slack_api.views_update(slack_client, view_id, view)


def push_view(slack_client, trigger_id, view):
    reusable.slack_api.views_push(slack_client, trigger_id, view)


def build_view_response(view):
    res = {'response_action': 'update', 'view': view}
    res = Response(
        json.dumps(res),
        mimetype='application/json',
        status=200)
    return res


def open_exception_view(slack_client, trigger_id, msg):
    exception_view = views.build_exception_view(msg)
    open_view(slack_client, trigger_id, exception_view)


def update_exception_view(slack_client, view_id, msg):
    exception_view = views.build_exception_view(msg)
    update_view(slack_client, view_id, exception_view)


def push_exception_view(slack_client, trigger_id, msg):
    exception_view = views.build_exception_view(msg)
    push_view(slack_client, trigger_id, exception_view)


def build_exception_view_response(msg):
    exception_view = views.build_exception_view(msg)
    return build_view_response(exception_view)


class SlackOperator:
    def __init__(self, game):
        self.game = game
        self.slack_client = self.game.slack_client
        self.block_builder = blocks.BlockBuilder(game)
        self.view_builder = views.ViewBuilder(game)
        self.tagging = self.game.exists and self.game.tagging

    def add_tag_to_text(self, text):
        if self.tagging:
            text = tag.add_tag_to_text(text, self.game.tag)
        return text

    def add_tag_to_blocks(self, blocks_):
        if self.tagging:
            blocks_ = tag.add_tag_to_json_list(blocks_, self.game.tag)
        return blocks_

    def add_tag_to_view(self, view):
        if self.tagging:
            view = tag.add_tag_to_json(view, self.game.tag)
        return view

    def get_app_user_id(self):
        return auth_test(self.slack_client)['user_id']

    def post_message(self, blocks_):
        blocks_ = self.add_tag_to_blocks(blocks_)
        return post_message(
            self.slack_client, self.game.channel_id, blocks_)

    def post_ephemeral(self, user_id, msg):
        msg = self.add_tag_to_text(msg)
        post_ephemeral(
            self.slack_client, self.game.channel_id, user_id, msg)

    def update_message(self, blocks_, ts):
        blocks_ = self.add_tag_to_blocks(blocks_)
        update_message(self.slack_client, self.game.channel_id,
                       blocks_, ts)

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
        open_exception_view(self.slack_client, trigger_id, msg)

    def update_exception_view(self, view_id, msg):
        msg = self.add_tag_to_text(msg)
        update_exception_view(self.slack_client, view_id, msg)

    def push_exception_view(self, trigger_id, msg):
        msg = self.add_tag_to_text(msg)
        push_exception_view(self.slack_client, trigger_id, msg)

    def build_exception_view_response(self, msg):
        msg = self.add_tag_to_text(msg)
        return build_exception_view_response(msg)

    def update_upper(self, blocks_):
        self.update_message(blocks_, self.game.upper_ts)

    def update_lower(self, blocks_):
        self.update_message(blocks_, self.game.lower_ts)

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
        msg = help.build_msg(self.game)
        self.post_ephemeral(user_id, msg)

    def send_vote_reminders(self):
        for u in self.game.potential_voters:
            msg = (
                f'Hey {users.user_display(u)}, '
                'you can now vote in the fictionary game '
                f'organized by {users.user_display(self.game.organizer_id)}!')
            self.post_ephemeral(u, msg)

    def send_is_over_notifications(self):
        for u in self.game.frozen_guessers:
            msg = ("The fictionary game organized by "
                   f"{users.user_display(self.game.organizer_id)} is over!")
            self.post_ephemeral(u, msg)

    def post_pre_guess_stage_upper(self):
        return self.post_message(
            self.block_builder.build_pre_guess_stage_upper_blocks())

    def post_pre_guess_stage_lower(self):
        return self.post_message(
            self.block_builder.build_pre_guess_stage_lower_blocks())

    def update_pre_vote_stage_upper(self):
        self.update_upper(
            self.block_builder.build_pre_vote_stage_upper_blocks())

    def update_pre_vote_stage_lower(self):
        self.update_lower(
            self.block_builder.build_pre_vote_stage_lower_blocks())

    def update_pre_result_stage_upper(self):
        self.update_upper(
            self.block_builder.build_pre_result_stage_upper_blocks())

    def update_pre_result_stage_lower(self):
        self.update_lower(
            self.block_builder.build_pre_result_stage_lower_blocks())

    def update_guess_stage_upper(self):
        self.update_upper(
            self.block_builder.build_guess_stage_upper_blocks())

    def update_guess_stage_lower(self):
        self.update_lower(
            self.block_builder.build_guess_stage_lower_blocks())

    def update_vote_stage_upper(self):
        self.update_upper(
            self.block_builder.build_vote_stage_upper_blocks())

    def update_vote_stage_lower(self):
        self.update_lower(
            self.block_builder.build_vote_stage_lower_blocks())

    def update_result_stage_upper(self):
        self.update_upper(
            self.block_builder.build_result_stage_upper_blocks())

    def update_result_stage_lower(self):
        self.update_lower(
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
