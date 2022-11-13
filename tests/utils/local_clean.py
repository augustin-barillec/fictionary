import reusable
import utils


def clean_cypress():
    reusable.processes.kill_processes('cypress')
    reusable.delete_local.delete_folder_if_exists('cypress/screenshots')


def clean_run_logs():
    reusable.delete_local.delete_file_if_exists(
        utils.local_paths.run_logs_file)


def clean():
    clean_cypress()
    clean_run_logs()
