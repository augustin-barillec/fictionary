import logging
import reusable
logger = logging.getLogger(__name__)


def store_team_params(team_ref, params):
    logger.info(f'Storing params for {team_ref.id}...')
    team_ref.set(params, merge=True)
    logger.info(f'Stored params for team {team_ref.id}')


def clean_channels_in_firestore(channels_ref):
    logger.info('Deleting channels in firestore...')
    cnt = 0
    for channel in channels_ref.stream():
        channel.reference.delete()
        logger.info(f'{channel.id} deleted')
        cnt += 1
    logger.info(f'Deleted {cnt} channels in firestore')


def store_channel_params(channels_ref, channel_id, params):
    logger.info(f'Storing params for channel_id = {channel_id}...')
    channel_ref = channels_ref.document(channel_id)
    channel_ref.set(params, merge=False)
    logger.info(f'Stored params for channel_id = {channel_id}')


def store_channel_name(channels_ref, channel_id, channel_name):
    logger.info('Storing channel_name...')
    channel_ref = channels_ref.document(channel_id)
    channel_ref.set({'channel_name': channel_name}, merge=True)
    logger.info('Stored channel_name')


def get_channel_id(channels_ref, channel_name):
    channel_dicts = reusable.firestore.get_dicts(channels_ref)
    for channel_id in channel_dicts:
        if channel_dicts[channel_id]['channel_name'] == channel_name:
            return channel_id
    raise ValueError(f'No channel_id matching {channel_name}')
