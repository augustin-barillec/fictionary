import argparse
import logging
import google.cloud.storage
import google.cloud.firestore
import reusable
import utils
import run_functions as rf
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level='INFO')
logger = logging.getLogger()
parser = argparse.ArgumentParser()
parser.add_argument('project_id')
args = parser.parse_args()
bucket_name = f'tests-{args.project_id}'
bucket_dir_name = reusable.time.get_now_compact_format()
timeout = 600
storage_client = google.cloud.storage.Client(project=args.project_id)
bucket = storage_client.bucket(bucket_name)
cypress_context_conf = utils.secret_manager.access_payload_parsed(
    args.project_id, 'cypress_context_conf')
team_id = cypress_context_conf['team_id']
db = google.cloud.firestore.Client(project=args.project_id)
teams_ref = db.collection('teams')
team_ref = teams_ref.document(team_id)
games_ref = team_ref.collection('games')
first_sources = [
    'small.cy.js',
    'exceptions/slash_command/max_running.cy.js',
    'exceptions/setup_submission/max_running.cy.js'
]
last_sources = [
    'endings/bravo.cy.js',
    'endings/hey.cy.js',
    'endings/no_guesses.cy.js',
    'endings/no_votes.cy.js',
    'endings/thanks.cy.js',
    'endings/well.cy.js',
    'endings/winner.cy.js',
    'endings/winners.cy.js',
    'endings/zero.cy.js',
    'exceptions/game_dead/open_view.cy.js',
    'exceptions/game_dead/update_view.cy.js',
    'exceptions/game_dead/view_response.cy.js',
    'exceptions/guess_click/already_guessed.cy.js',
    'exceptions/guess_click/organizer.cy.js',
    'exceptions/guess_submission/max_these_guessers.cy.js',
    'exceptions/guess_submission/no_time_left.cy.js',
    'exceptions/pick_submission/not_between.cy.js',
    'exceptions/pick_submission/not_integer.cy.js',
    'exceptions/setup_submission/max_this_running.cy.js',
    'exceptions/slash_command/invalid_parameter.cy.js',
    'exceptions/slash_command/max_this_running.cy.js',
    'exceptions/slash_command/not_invited.cy.js',
    'exceptions/vote_click/already_voted.cy.js',
    'exceptions/vote_click/not_a_potential_voter.cy.js',
    'exceptions/vote_submission/no_time_left.cy.js',
    'setups/english.cy.js',
    'setups/freestyle.cy.js',
    'setups/french.cy.js',
    'transitions/guess_full_time.cy.js',
    'transitions/guess_shorten_time.cy.js',
    'transitions/vote_full_time.cy.js',
    'transitions/vote_shorten_time.cy.js',
    'help.cy.js',
    'special_characters.cy.js'
]
sources = first_sources + last_sources
utils.local_clean.clean_cypress()
logger.info('Deleting games...')
cnt = 0
for g in games_ref.stream():
    g.reference.delete()
    cnt += 1
logger.info(f'Deleted {cnt} games')
logger.info(f'Starting run {len(sources)} tests...')
start_datetime = reusable.time.get_now()
for source in sources[:1]:
    rf.run_cypress(args.project_id, bucket, bucket_dir_name, source, timeout)
end_datetime = reusable.time.get_now()
duration = round((end_datetime - start_datetime).total_seconds())
logger.info(f'Ended run tests [{duration}s]')
rf.write_stats(bucket, bucket_dir_name)
rf.report_successes(bucket, bucket_dir_name)
rf.report_fails(bucket, bucket_dir_name)
rf.upload_run_logs_if_exists(bucket, bucket_dir_name)
