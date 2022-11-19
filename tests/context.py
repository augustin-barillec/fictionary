import argparse
import google.cloud.firestore
import reusable
import utils
import context_functions as cf
import channels
logger = reusable.root_logger.configure_root_logger()
parser = argparse.ArgumentParser()
parser.add_argument('project_id')
subparsers = parser.add_subparsers(dest='command')
subparsers.add_parser('setup_team')
subparsers.add_parser('setup_channels')
subparsers.add_parser('print_conf')
get_channel_id_parser = subparsers.add_parser('print_channel_id')
get_channel_id_parser.add_argument('channel_name')
create_fake_guess_parser = subparsers.add_parser('create_fake_guess')
create_fake_guess_parser.add_argument('tag')
create_fake_guess_parser.add_argument('user_index', type=int)
create_fake_running_game_parser = subparsers.add_parser(
    'create_fake_running_game')
create_fake_running_game_parser.add_argument('organizer_index', type=int)
mark_game_as_success_parser = subparsers.add_parser('mark_game_as_success')
mark_game_as_success_parser.add_argument('tag')
delete_game_parser = subparsers.add_parser('delete_game')
delete_game_parser.add_argument('tag')
args = parser.parse_args()

cypress_context_conf = utils.secret_manager.access_payload_parsed(
    args.project_id, 'cypress_context_conf')
app_user_id = cypress_context_conf['app_user_id']
cypress_slack_token = cypress_context_conf['cypress_slack_token']
cypress_user_id = cypress_context_conf['cypress_user_id']
team_id = cypress_context_conf['team_id']
user_ids = utils.users.get_user_ids(cypress_context_conf)
db = google.cloud.firestore.Client(project=args.project_id)
teams_ref = db.collection('teams')
team_ref = teams_ref.document(team_id)
games_ref = team_ref.collection('games')
channels_ref = team_ref.collection('channels')

if args.command == 'setup_team':
    cf.setup_team(team_ref)
elif args.command == 'setup_channels':
    from slack_sdk import WebClient
    slack_client = WebClient(cypress_slack_token)
    cf.setup_channels(
        slack_client,
        channels_ref,
        channels.channel_names,
        channels.channel_to_params,
        channels.channel_to_user_indexes,
        channels.channel_to_app_kicked,
        user_ids,
        app_user_id,
        cypress_user_id)
elif args.command == 'print_conf':
    print(cypress_context_conf)
elif args.command == 'print_channel_id':
    print(cf.get_channel_id(channels_ref, args.channel_name))
elif args.command == 'create_fake_guess':
    user_id = user_ids[args.user_index]
    cf.create_fake_guess(games_ref, args.tag, user_id)
elif args.command == 'create_fake_running_game':
    organizer_id = user_ids[args.organizer_index]
    cf.create_fake_running_game(games_ref, organizer_id)
elif args.command == 'mark_game_as_success':
    cf.mark_game_as_success(games_ref, args.tag)
elif args.command == 'delete_game':
    cf.delete_game(games_ref, args.tag)
