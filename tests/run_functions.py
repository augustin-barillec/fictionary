import glob
import logging
import subprocess
import os
import reusable
import utils
logger = logging.getLogger(__name__)
command_template = """
DEBUG=cypress:server npx cypress run \
--headless \
--browser chrome \
--env PROJECT_ID={project_id} \
--spec {spec}
"""


def delete_screenshots_dir_if_exists():
    screenshots_path = 'cypress/screenshots'
    reusable.delete_local.delete_folder_if_exists(screenshots_path)


def build_spec(source):
    return f'cypress/e2e/{source}'


def run_cypress(project_id, bucket, bucket_dir_name, source, timeout):
    logger.info(f'Running {source} on {project_id}...')
    spec = build_spec(source)
    assert os.path.exists(spec)
    command = command_template.format(project_id=project_id, spec=spec)
    source_rewritten = source.replace('/', '&')
    source_basename = source.split('/')[-1]
    try:
        completed_process = subprocess.run(
            command, shell=True, timeout=timeout)
        assert completed_process.returncode in (0, 1)
    except subprocess.TimeoutExpired:
        completed_process = None
        reusable.processes.kill_processes('Cypress')
    if completed_process is not None and completed_process.returncode == 0:
        msg = f'success#{source_rewritten}'
        logger.info(msg)
        utils.storage.upload_string_to_gs(
            bucket, bucket_dir_name, msg, msg)
    elif completed_process is None or completed_process.returncode == 1:
        msg = f'fail#{source_rewritten}'
        logger.info(msg)
        utils.storage.upload_string_to_gs(bucket, bucket_dir_name, msg, msg)
        if completed_process is None:
            msg = f'TimeoutExpired#{source_rewritten}'
            logger.info(msg)
            utils.storage.upload_string_to_gs(
                bucket, bucket_dir_name, msg, msg)
        screenshot_paths = glob.glob(
            f'cypress/screenshots/{source_basename}/*.png')
        logger.info(f'screenshot_paths = {screenshot_paths}')
        if len(screenshot_paths) >= 1:
            screenshot_path = screenshot_paths[0]
            screenshot_blob_basename = f'screenshot#{source_rewritten}'
            utils.storage.upload_file_to_gs(
                bucket, bucket_dir_name,
                screenshot_blob_basename, screenshot_path)
            logger.info(f'{screenshot_blob_basename} uploaded')
    logger.info(f'Ran {source} on {project_id}')


def get_outcomes(bucket, bucket_dir_name, kind):
    assert kind in ('success', 'fail')
    prefix = f'{bucket_dir_name}/{kind}#'
    res = list(bucket.list_blobs(prefix=prefix))
    res = [blob.name for blob in res]
    res = [blob_name.split('#')[-1] for blob_name in res]
    return res


def get_successes(bucket, bucket_dir_name):
    return get_outcomes(bucket, bucket_dir_name, 'success')


def get_fails(bucket, bucket_dir_name):
    return get_outcomes(bucket, bucket_dir_name, 'fail')


def write_stats(bucket, bucket_dir_name):
    nb_successes = len(get_successes(bucket, bucket_dir_name))
    nb_fails = len(get_fails(bucket, bucket_dir_name))
    nb_cases = nb_successes + nb_fails
    ratio = nb_successes / nb_cases
    stats = {
        'nb_cases': nb_cases,
        'nb_successes': nb_successes,
        'nb_fails': nb_fails,
        'ratio': ratio}
    logger.info(f'stats={stats}')
    utils.storage.upload_string_to_gs(
        bucket, bucket_dir_name, 'stats', str(stats))


def report(bucket, bucket_dir_name, kind):
    assert kind in ('success', 'fail')
    if kind == 'success':
        plural = 'successes'
    else:
        plural = 'fails'
    selected = globals()[f'get_{plural}'](bucket, bucket_dir_name)
    selected = [s.replace('&', '/') for s in selected]
    selected = [f"'{s}'" for s in selected]
    selected = ',\n'.join(selected)
    utils.storage.upload_string_to_gs(
        bucket, bucket_dir_name, f'report_{plural}', selected)


def report_successes(bucket, bucket_dir_name):
    report(bucket, bucket_dir_name, 'success')


def report_fails(bucket, bucket_dir_name):
    report(bucket, bucket_dir_name, 'fail')


def upload_run_logs_if_exists(bucket, bucket_dir_name):
    run_logs_basename = 'run.txt'
    if os.path.exists(run_logs_basename):
        utils.storage.upload_file_to_gs(
            bucket, bucket_dir_name, run_logs_basename, run_logs_basename)
