import logging
import argparse
import google.cloud.firestore
import utils
import context_functions as cf
import channels
from slack_sdk import WebClient
from reusable import secret_manager

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level='INFO')
logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
subparsers = parser.add_subparsers(dest='command')
subparsers.add_parser('setup_team')
subparsers.add_parser('setup_channels')
subparsers.add_parser('print_conf')
get_channel_id_parser = subparsers.add_parser('print_channel_id')
get_channel_id_parser.add_argument('channel_name')
subparsers.add_parser('clean_games')
create_fake_guesser_parser = subparsers.add_parser('create_fake_guesser')
create_fake_guesser_parser.add_argument('tag')
create_fake_running_game_parser = subparsers.add_parser(
    'create_fake_running_game')
create_fake_running_game_parser.add_argument('organizer_index', type=int)
delete_game_parser = subparsers.add_parser('delete_game')
delete_game_parser.add_argument('tag')
kick_from_channel_parser = subparsers.add_parser('kick_from_channel')
kick_from_channel_parser.add_argument('channel_id')
kick_from_channel_parser.add_argument('user_index', type=int)
invite_to_channel_parser = subparsers.add_parser('invite_to_channel')
invite_to_channel_parser.add_argument('channel_id')
invite_to_channel_parser.add_argument('user_index', type=int)
args = parser.parse_args()

cypress_context_conf = secret_manager.access_payload_parsed(
    args.project_id,
    'cypress_context_conf')
app_user_id = cypress_context_conf['app_user_id']
cypress_slack_token = cypress_context_conf['cypress_slack_token']
slack_client = WebClient(cypress_slack_token)
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
elif args.command == 'clean_games':
    cf.clean_games(games_ref)
elif args.command == 'create_fake_guesser':
    cf.create_fake_guesser(games_ref, args.tag)
elif args.command == 'create_fake_running_game':
    organizer_id = user_ids[args.organizer_index]
    cf.create_fake_running_game(games_ref, organizer_id)
elif args.command == 'delete_game':
    cf.delete_game(games_ref, args.tag)
elif args.command == 'kick_from_channel':
    user_id = user_ids[args.user_index]
    cf.kick_from_channel(slack_client, args.channel_id, user_id)
elif args.command == 'invite_to_channel':
    user_id = user_ids[args.user_index]
    cf.invite_to_channel(slack_client, args.channel_id, user_id)
