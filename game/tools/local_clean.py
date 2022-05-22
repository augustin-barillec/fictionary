import os
import shutil
from reusable import processes
from tools import local_paths, ports


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_files(file_paths):
    for p in file_paths:
        delete_file(p)


def delete_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)


def clean_cloud_deploy_functions():
    processes.kill_processes('gcloud.py alpha functions deploy')
    for port in ports.ports:
        filepath = local_paths.cloud_deploy_function_file.format(port=port)
        delete_file(filepath)


def clean_pubsub():
    data_dir_path = local_paths.pubsub_data_dir
    delete_folder(data_dir_path)
    processes.kill_processes('pubsub-emulator')
    processes.kill_processes('emulators pubsub')


def clean_functions():
    port_to_function_name = ports.port_to_function_name
    for port in ports.ports:
        local_function_filepath = local_paths.local_function_file.format(
            port=port)
        function_name = port_to_function_name[port]
        delete_file(local_function_filepath)
        processes.kill_processes(
            f'--target {function_name}')


def clean_daily():
    clean_cloud_deploy_functions()
    clean_pubsub()
    clean_functions()
