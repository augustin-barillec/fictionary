import datetime
import google.cloud.bigquery
import pandas
import reusable
import app.utils as ut

columns = [
    'outcome',
    'team_id',
    'channel_id',
    'organizer_id',
    'parameter',
    'question',
    'truth',
    'slash_datetime',
    'setup_submission',
    'nb_guessers',
    'nb_voters',
    'version',
    'game_id']

bq_schema = [
    google.cloud.bigquery.SchemaField('outcome', 'STRING'),
    google.cloud.bigquery.SchemaField('team_id', 'STRING'),
    google.cloud.bigquery.SchemaField('channel_id', 'STRING'),
    google.cloud.bigquery.SchemaField('organizer_id', 'STRING'),
    google.cloud.bigquery.SchemaField('parameter', 'STRING'),
    google.cloud.bigquery.SchemaField('question', 'STRING'),
    google.cloud.bigquery.SchemaField('truth', 'STRING'),
    google.cloud.bigquery.SchemaField('slash_datetime', 'TIMESTAMP'),
    google.cloud.bigquery.SchemaField('setup_submission', 'TIMESTAMP'),
    google.cloud.bigquery.SchemaField('nb_guessers', 'INTEGER'),
    google.cloud.bigquery.SchemaField('nb_voters', 'INTEGER'),
    google.cloud.bigquery.SchemaField('version', 'STRING'),
    google.cloud.bigquery.SchemaField('game_id', 'STRING')]


def compute_row(game_id, game_dict, outcome):
    row = dict()
    team_id = ut.ids.game_id_to_team_id(game_id)
    channel_id = ut.ids.game_id_to_channel_id(game_id)
    organizer_id = ut.ids.game_id_to_organizer_id(game_id)
    slash_datetime_compact = ut.ids.game_id_to_slash_datetime_compact(
        game_id)
    slash_datetime = reusable.time.compact_to_datetime(slash_datetime_compact)
    setup_submission = game_dict.get('setup_submission')
    parameter = game_dict.get('parameter')
    assert parameter in ('freestyle', 'automatic')
    question = None
    truth = None
    if parameter == 'automatic':
        question = game_dict.get('question')
        truth = game_dict.get('truth')
    if 'frozen_guessers' in game_dict:
        nb_guessers = len(game_dict['frozen_guessers'])
    else:
        nb_guessers = None
    if 'frozen_voters' in game_dict:
        nb_voters = len(game_dict['frozen_voters'])
    else:
        nb_voters = None
    version = game_dict.get('version')
    row['outcome'] = outcome
    row['team_id'] = team_id
    row['channel_id'] = channel_id
    row['organizer_id'] = organizer_id
    row['parameter'] = parameter
    row['question'] = question
    row['truth'] = truth
    row['slash_datetime'] = slash_datetime
    row['setup_submission'] = setup_submission
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
    today_no_dash = str(
        datetime.datetime.now(datetime.timezone.utc).date()).replace('-', '')
    dataset_id = f'{project_id}.monitoring'
    destination_table_id = f'{dataset_id}.monitoring_{today_no_dash}'
    job_config = google.cloud.bigquery.LoadJobConfig(
        schema=bq_schema,
        write_disposition='WRITE_APPEND')
    job = bq_client.load_table_from_dataframe(
        monitoring, destination_table_id, job_config=job_config)
    job.result()
