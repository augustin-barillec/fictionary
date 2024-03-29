import logging
import reusable
import utils
logger = logging.getLogger(__name__)


def setup_channels(
        slack_client,
        channels_ref,
        channel_names,
        channel_name_to_params,
        channel_name_to_user_indexes,
        channel_name_to_app_kicked,
        cypress_user_id,
        app_user_id,
        user_ids):
    utils.firestore.clean_channels_in_firestore(channels_ref)
    channel_name_to_channel_id = dict()
    for channel_name in channel_names:
        logger.info(f'Setting {channel_name}...')
        params = channel_name_to_params[channel_name]
        user_indexes = channel_name_to_user_indexes[channel_name]
        app_kicked = channel_name_to_app_kicked[channel_name]
        channels = utils.slack.list_channels(slack_client)
        if not utils.slack.channel_exists(channels, channel_name):
            channel_id = utils.slack.create_channel(slack_client, channel_name)
        else:
            channel_id = utils.slack.get_channel_id(channels, channel_name)
        channel_name_to_channel_id[channel_name] = channel_id
        if not utils.slack.is_member(
                slack_client, channel_id, cypress_user_id):
            utils.slack.join(slack_client, channel_id)
        utils.slack.kick_all(slack_client, channel_id, [cypress_user_id])
        utils.slack.invite(slack_client, channel_id, [app_user_id])
        user_ids_to_invite = [user_ids[i] for i in user_indexes]
        utils.slack.invite(slack_client, channel_id, user_ids_to_invite)
        if app_kicked:
            utils.slack.kick(slack_client, channel_id, [app_user_id])
        utils.firestore.store_channel_params(
            channels_ref, channel_id, params)
        utils.firestore.store_channel_name(
            channels_ref, channel_id, channel_name)
        utils.slack.leave(slack_client, channel_id)
        logger.info(f'Set {channel_name}')


def get_channel_id(channel_refs, channel_name):
    return utils.firestore.get_channel_id(channel_refs, channel_name)


def create_fake_guess(games_ref, tag, user_id):
    game_dicts = reusable.firestore.get_dicts(games_ref)
    for game_id in game_dicts:
        game_dict = game_dicts[game_id]
        if game_dict['tag'] == tag:
            game_ref = games_ref.document(game_id)
            now = reusable.time.get_now()
            game_ref.update({f'guessers.{user_id}': [now, 'fake_guess']})


def create_fake_running_game(games_ref, tag, organizer_id):
    slash_datetime_compact = reusable.time.get_now_compact_format()
    game_id = reusable.ids.build_game_id(
        slash_datetime_compact, 'team_id',
        'channel_id', organizer_id, 'trigger_id')
    game_dict = {
        'tag': tag,
        'parameter': 'freestyle',
        'setup_submission': reusable.time.get_now()}
    game_ref = games_ref.document(game_id)
    game_ref.set(game_dict, merge=False)


def mark_game_as_success(games_ref, tag):
    cnt = 0
    for g in games_ref.stream():
        game_dict = g.to_dict()
        if game_dict['tag'] == tag:
            game_dict['result_stage_over'] = True
            g.reference.set(game_dict, merge=False)
            cnt += 1
    assert cnt == 1


def delete_game(games_ref, tag):
    cnt = 0
    for g in games_ref.stream():
        game_dict = g.to_dict()
        if game_dict['tag'] == tag:
            g.reference.delete()
            cnt += 1
    assert cnt == 1
