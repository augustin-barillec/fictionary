import logging
import argparse
import google.cloud.storage
import run_functions as rf

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level='INFO')
logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('project_id')
parser.add_argument('bucket_name')
parser.add_argument('bucket_dir_name')
subparsers = parser.add_subparsers(dest='command')
run_cypress_parser = subparsers.add_parser('run_cypress')
run_cypress_parser.add_argument('source')
run_cypress_parser.add_argument('timeout', type=int)
wait_end_parser = subparsers.add_parser('wait_end')
wait_end_parser.add_argument('expected_nb_cases', type=int)
subparsers.add_parser('write_stats')
subparsers.add_parser('report_successes')
subparsers.add_parser('report_fails')
args = parser.parse_args()

storage_client = google.cloud.storage.Client(project=args.project_id)
bucket = storage_client.bucket(args.bucket_name)

assert args.command in (
    'run_cypress', 'wait_end', 'write_stats',
    'report_successes', 'report_fails')
if args.command == 'run_cypress':
    rf.run_cypress(
        args.project_id, bucket, args.bucket_dir_name,
        args.source, args.timeout)
elif args.command == 'wait_end':
    rf.wait_end(bucket, args.bucket_dir_name, args.expected_nb_cases)
elif args.command == 'write_stats':
    rf.write_stats(bucket, args.bucket_dir_name)
elif args.command == 'report_successes':
    rf.report_successes(bucket, args.bucket_dir_name)
elif args.command == 'report_fails':
    rf.report_fails(bucket, args.bucket_dir_name)
