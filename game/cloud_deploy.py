import argparse
import logging
import tools
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level='INFO')
logger = logging.getLogger()
parser = argparse.ArgumentParser()
parser.add_argument('project_id')
subparsers = parser.add_subparsers(dest='to_deploy')
subparsers.add_parser('pubsub')
functions_parser = subparsers.add_parser('function')
functions_parser.add_argument('region')
functions_parser.add_argument('port', type=int)
functions_parser.add_argument('pre_sleep_duration', type=int)
args = parser.parse_args()
assert args.to_deploy in ('pubsub', 'function')
if args.to_deploy == 'pubsub':
    tools.cloud_deploy.deploy_pubsub(args.project_id)
elif args.to_deploy == 'function':
    tools.cloud_deploy.deploy_function(
        args.project_id, args.region, args.port, args.pre_sleep_duration)
