import pandas
import reusable
from google.cloud import bigquery
from app import utils

columns = [
    'outcome',
    'team_id',
    'channel_id',
    'organizer_id',
    'slash_datetime',
    'setup_submission',
    'max_guessers',
    'nb_guessers',
    'nb_voters',
    'version',
    'game_id']

bq_schema = [
    bigquery.SchemaField('outcome', 'STRING'),
    bigquery.SchemaField('team_id', 'STRING'),
    bigquery.SchemaField('channel_id', 'STRING'),
    bigquery.SchemaField('organizer_id', 'STRING'),
    bigquery.SchemaField('slash_datetime', 'TIMESTAMP'),
    bigquery.SchemaField('setup_submission', 'TIMESTAMP'),
    bigquery.SchemaField('max_guessers', 'INTEGER'),
    bigquery.SchemaField('nb_guessers', 'INTEGER'),
    bigquery.SchemaField('nb_voters', 'INTEGER'),
    bigquery.SchemaField('version', 'STRING'),
    bigquery.SchemaField('game_id', 'STRING')]


def compute_row(game_id, game_dict, outcome):
    row = dict()
    team_id = utils.ids.game_id_to_team_id(game_id)
    channel_id = utils.ids.game_id_to_channel_id(game_id)
    organizer_id = utils.ids.game_id_to_organizer_id(game_id)
    slash_datetime_compact = utils.ids.game_id_to_slash_datetime_compact(
        game_id)
    slash_datetime = reusable.time.compact_to_datetime(slash_datetime_compact)
    setup_submission = game_dict.get('setup_submission')
    max_guessers = game_dict.get('max_guessers')
    if 'frozen_guessers' in game_dict:
        nb_guessers = len(game_dict['frozen_guessers'])
    else:
        nb_guessers = None
    if 'frozen_voters' in game_dict:
        nb_voters = len(game_dict['frozen_voters'])
    else:
        nb_voters = None
    version = game_dict['version']
    row['outcome'] = outcome
    row['team_id'] = team_id
    row['channel_id'] = channel_id
    row['organizer_id'] = organizer_id
    row['slash_datetime'] = slash_datetime
    row['setup_submission'] = setup_submission
    row['max_guessers'] = max_guessers
    row['nb_guessers'] = nb_guessers
    row['nb_voters'] = nb_voters
    row['version'] = version
    row['game_id'] = game_id
    return row


def compute_monitoring(game_ids, game_dicts, outcomes):
    assert len(game_ids) == len(game_dicts) == len(outcomes)
    rows = []
    for game_id, game_dict, outcome in zip(game_ids, game_dicts, outcomes):
        row = compute_row(game_id, game_dict, outcome)
        rows.append(row)
    return pandas.DataFrame(data=rows, columns=columns)


def upload_monitoring(bq_client, project_id, monitoring):
    destination_table_id = f'{project_id}.monitoring.monitoring'
    job_config = bigquery.LoadJobConfig(
        schema=bq_schema,
        write_disposition='WRITE_APPEND')
    job = bq_client.load_table_from_dataframe(
        monitoring, destination_table_id, job_config=job_config)
    job.result()


def deduplicate_monitoring(bq_client, project_id):
    query = f"""
    select * from {project_id}.monitoring.monitoring
    qualify row_number() over (partition by game_id) = 1
    """
    destination_table_id = f'{project_id}.monitoring.monitoring'
    job_config = bigquery.QueryJobConfig()
    job_config.destination = destination_table_id
    job_config.write_disposition = 'WRITE_TRUNCATE'
    job = bq_client.query(query=query, job_config=job_config)
    job.result()
