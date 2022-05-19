import argparse
import tools

parser = argparse.ArgumentParser()
parser.add_argument('to_clean')
args = parser.parse_args()

assert args.to_clean in ('pubsub', 'functions', 'daily')
getattr(tools.local_clean, 'clean_' + args.to_clean)()
