import logging
import utils
logger = logging.getLogger(__name__)


def list_channels(slack_client):
    resp = utils.slack_api.conversations_list(slack_client)
    channels = resp['channels']
    channels = [(c['id'], c['name']) for c in channels]
    return channels


def channel_exists(channels, channel_name):
    return channel_name in [c[1] for c in channels]


def get_channel_id(channels, channel_name):
    assert channel_exists(channels, channel_name)
    for channel_id_, channel_name_ in channels:
        if channel_name == channel_name_:
            return channel_id_


def list_members(slack_client, channel_id):
    resp = utils.slack_api.conversations_members(
        slack_client, channel_id)
    return list(resp['members'])


def is_member(slack_client, channel_id, user_id):
    members = list_members(slack_client, channel_id)
    return user_id in members


def create_channel(slack_client, channel_name):
    logger.info(f'Starting create {channel_name}...')
    resp = utils.slack_api.conversations_create(
        slack_client, channel_name)
    channel_id = resp['channel']['id']
    logger.info(f'Ended create {channel_name} with channel_id = {channel_id}')
    return channel_id


def kick(slack_client, channel_id, user_ids):
    logger.info(f'Starting kick {user_ids} from {channel_id}...')
    for user_id in user_ids:
        logger.info(f'Kicking {user_id}...')
        utils.slack_api.conversations_kick(slack_client, channel_id, user_id)
        logger.info(f'Kicked {user_id}')
    logger.info(f'Ended kick {user_ids} from {channel_id}')


def kick_all(slack_client, channel_id, except_):
    logger.info(f'Starting kick_all from {channel_id}...')
    members = list_members(slack_client, channel_id)
    to_kick = [m for m in members if m not in except_]
    kick(slack_client, channel_id, to_kick)
    logger.info(f'Ended kick_all from {channel_id}')


def invite(slack_client, channel_id, user_ids):
    logger.info(f'Starting invite {user_ids} to {channel_id}...')
    for user_id in user_ids:
        logger.info(f'Inviting {user_id}...')
        utils.slack_api.conversations_invite(slack_client, channel_id, user_id)
        logger.info(f'Invited {user_id}')
    logger.info(f'Ended invite {user_ids} to {channel_id}')


def join(slack_client, channel_id):
    logger.info(f'Starting join {channel_id}...')
    utils.slack_api.conversations_join(slack_client, channel_id)
    logger.info(f'Ended join {channel_id}')


def leave(slack_client, channel_id):
    logger.info('Starting leave...')
    utils.slack_api.conversations_leave(slack_client, channel_id)
    logger.info('Ended leave')
