import argparse
import logging
import tools
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level='INFO')
logger = logging.getLogger()
parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
parser.add_argument('to_deploy')
args = parser.parse_args()
assert args.to_deploy in ('pubsub', 'functions')
getattr(tools.local_deploy, 'deploy_' + args.to_deploy)(args.project_id)
