import argparse
import google.cloud.storage
import google.cloud.firestore
import reusable
import utils
import run_functions as rf
logger = reusable.root_logger.configure_root_logger()
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
sources = [
    'small.cy.js',

    'english/endings/draw.cy.js',
    'english/endings/no_guesses.cy.js',
    'english/endings/no_votes.cy.js',
    'english/endings/one_guesser.cy.js',
    'english/endings/one_voter_loser.cy.js',
    'english/endings/one_voter_winner.cy.js',
    'english/endings/winner.cy.js',
    'english/endings/winners.cy.js',
    'english/endings/zero.cy.js',
    'english/exceptions/game_dead/open_view.cy.js',
    'english/exceptions/game_dead/update_view.cy.js',
    'english/exceptions/game_dead/view_response.cy.js',
    'english/exceptions/guess_click/already_guessed.cy.js',
    'english/exceptions/guess_click/organizer.cy.js',
    'english/exceptions/guess_submission/max_these_guessers.cy.js',
    'english/exceptions/guess_submission/no_time_left.cy.js',
    'english/exceptions/pick_submission/not_between.cy.js',
    'english/exceptions/pick_submission/not_integer.cy.js',
    'english/exceptions/setup_submission/max_running.cy.js',
    'english/exceptions/setup_submission/max_this_running.cy.js',
    'english/exceptions/slash_command/invalid_parameter.cy.js',
    'english/exceptions/slash_command/max_running.cy.js',
    'english/exceptions/slash_command/max_this_running.cy.js',
    'english/exceptions/slash_command/not_invited.cy.js',
    'english/exceptions/vote_click/already_voted.cy.js',
    'english/exceptions/vote_click/not_a_potential_voter.cy.js',
    'english/exceptions/vote_submission/no_time_left.cy.js',
    'english/setups/automatic_pick.cy.js',
    'english/setups/automatic_shuffle.cy.js',
    'english/setups/freestyle.cy.js',
    'english/transitions/guess_full_time.cy.js',
    'english/transitions/guess_shorten_time.cy.js',
    'english/transitions/vote_full_time.cy.js',
    'english/transitions/vote_shorten_time.cy.js',
    'english/help.cy.js',
    'english/special_characters.cy.js',

    'french/endings/draw.cy.js',
    'french/endings/no_guesses.cy.js',
    'french/endings/no_votes.cy.js',
    'french/endings/one_guesser.cy.js',
    'french/endings/one_voter_loser.cy.js',
    'french/endings/one_voter_winner.cy.js',
    'french/endings/winner.cy.js',
    'french/endings/winners.cy.js',
    'french/endings/zero.cy.js',
    'french/exceptions/game_dead/open_view.cy.js',
    'french/exceptions/game_dead/update_view.cy.js',
    'french/exceptions/game_dead/view_response.cy.js',
    'french/exceptions/guess_click/already_guessed.cy.js',
    'french/exceptions/guess_click/organizer.cy.js',
    'french/exceptions/guess_submission/max_these_guessers.cy.js',
    'french/exceptions/guess_submission/no_time_left.cy.js',
    'french/exceptions/pick_submission/not_between.cy.js',
    'french/exceptions/pick_submission/not_integer.cy.js',
    'french/exceptions/setup_submission/max_running.cy.js',
    'french/exceptions/setup_submission/max_this_running.cy.js',
    'french/exceptions/slash_command/invalid_parameter.cy.js',
    'french/exceptions/slash_command/max_running.cy.js',
    'french/exceptions/slash_command/max_this_running.cy.js',
    'french/exceptions/slash_command/not_invited.cy.js',
    'french/exceptions/vote_click/already_voted.cy.js',
    'french/exceptions/vote_click/not_a_potential_voter.cy.js',
    'french/exceptions/vote_submission/no_time_left.cy.js',
    'french/setups/automatic_pick.cy.js',
    'french/setups/automatic_shuffle.cy.js',
    'french/setups/freestyle.cy.js',
    'french/transitions/guess_full_time.cy.js',
    'french/transitions/guess_shorten_time.cy.js',
    'french/transitions/vote_full_time.cy.js',
    'french/transitions/vote_shorten_time.cy.js',
    'french/help.cy.js',
    'french/special_characters.cy.js'
]
len_sources = len(sources)
utils.local_clean.clean_cypress()
logger.info('Deleting games...')
cnt = 0
for g in games_ref.stream():
    g.reference.delete()
    cnt += 1
logger.info(f'Deleted {cnt} games')
logger.info(f'Starting run these {len_sources} tests: {sources}...')
start_datetime = reusable.time.get_now()
for i, source in enumerate(sources, 1):
    logger.info(f'Starting test {i}/{len_sources}...')
    rf.run_cypress(args.project_id, bucket, bucket_dir_name, source, timeout)
    logger.info(f'Ended test {i}/{len_sources}')
end_datetime = reusable.time.get_now()
duration = round((end_datetime - start_datetime).total_seconds())
logger.info(f'Ended run tests [{duration}s]')
rf.write_stats(bucket, bucket_dir_name)
rf.report_successes(bucket, bucket_dir_name)
rf.report_fails(bucket, bucket_dir_name)
rf.upload_run_logs_if_exists(bucket, bucket_dir_name)
