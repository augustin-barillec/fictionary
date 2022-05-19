import argparse
import logging
import tools

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level='INFO')
logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
parser.add_argument('--region')
subparsers = parser.add_subparsers(dest='command')
local_parser = subparsers.add_parser('local')
local_parser.add_argument('to_deploy')
cloud_parser = subparsers.add_parser('cloud')
cloud_parser.add_argument('to_deploy')
cloud_parser.add_argument('--single_port', type=int)
cloud_parser.add_argument('--pre_sleep_duration', type=int)
args = parser.parse_args()

assert args.command in ('local', 'cloud')
assert args.to_deploy in ('pubsub', 'functions')
if args.command == 'local':
    getattr(tools.local_deploy, 'deploy_' + args.to_deploy)(args.project_id)
elif args.command == 'cloud':
    f = getattr(tools.cloud_deploy, 'deploy_' + args.to_deploy)
    if args.to_deploy == 'pubsub':
        f(args.project_id)
    elif args.to_deploy == 'functions':
        assert args.region is not None
        f(args.project_id, args.region,
          args.single_port, args.pre_sleep_duration)
