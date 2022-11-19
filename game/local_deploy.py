import argparse
import reusable
import tools
logger = reusable.root_logger.configure_root_logger()
parser = argparse.ArgumentParser()
parser.add_argument('project_id')
parser.add_argument('to_deploy')
args = parser.parse_args()
assert args.to_deploy in ('pubsub', 'functions')
getattr(tools.local_deploy, 'deploy_' + args.to_deploy)(args.project_id)
