import logging
import reusable
import utils

logger = logging.getLogger(__name__)


def setup_channels(
        slack_client,
        channels_ref,
        channel_names,
        channel_to_params,
        channel_to_user_indexes,
        channel_to_app_kicked,
        user_ids,
        app_user_id,
        cypress_user_id):

    utils.firestore.clean_channels_in_firestore(channels_ref)

    channel_name_to_channel_id = dict()
    for channel_name in channel_names:
        logger.info(f'Setting {channel_name}...')
        params = channel_to_params[channel_name]
        user_indexes = channel_to_user_indexes[channel_name]
        app_kicked = channel_to_app_kicked[channel_name]
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
        logger.info(f'Set {channel_name}')


def get_channel_id(channel_refs, channel_name):
    return utils.firestore.get_channel_id(channel_refs, channel_name)


def clean_games(games_ref):
    utils.firestore.clean_games(games_ref)


def create_fake_guesser(games_ref, tag):
    game_dicts = reusable.firestore.get_dicts(games_ref)
    for game_id in game_dicts:
        game_dict = game_dicts[game_id]
        if game_dict['tag'] == tag:
            now = reusable.time.get_now()
            data = {'guessers': {f'guesser_id_{now}': [now, 'guess']}}
            game_ref = games_ref.document(game_id)
            game_ref.set(data, merge=True)


def create_fake_running_game(games_ref, organizer_id):
    slash_datetime_compact = reusable.time.get_now_compact_format()
    game_id = reusable.ids.build_game_id(
        slash_datetime_compact, 'team_id',
        'channel_id', organizer_id, 'trigger_id')
    game_dict = {
        'version': 1,
        'tag': 'tag',
        'setup_submission': reusable.time.get_now()}
    game_ref = games_ref.document(game_id)
    game_ref.set(game_dict, merge=False)


def kick_from_channel(slack_client, channel_id, user_id):
    if utils.slack.is_member(slack_client, channel_id, user_id):
        utils.slack.kick(slack_client, channel_id, [user_id])


def invite_to_channel(slack_client, channel_id, user_id):
    utils.slack.invite(slack_client, channel_id, [user_id])
