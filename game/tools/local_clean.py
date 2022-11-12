import reusable
import tools


def clean_cloud_deploy_functions():
    for port in tools.ports.ports:
        filepath = tools.local_paths.cloud_deploy_function_file.format(
            port=port)
        reusable.delete_local.delete_file_if_exists(filepath)


def clean_pubsub():
    data_dir_path = tools.local_paths.pubsub_data_dir
    reusable.delete_local.delete_folder_if_exists(data_dir_path)
    reusable.processes.kill_processes('pubsub-emulator')
    reusable.processes.kill_processes('emulators pubsub')


def clean_functions():
    port_to_function_name = tools.ports.port_to_function_name
    for port in tools.ports.ports:
        local_function_filepath = tools.local_paths.local_function_file.format(
            port=port)
        function_name = port_to_function_name[port]
        reusable.delete_local.delete_file_if_exists(local_function_filepath)
        reusable.processes.kill_processes(f'--target {function_name}')


def clean():
    clean_cloud_deploy_functions()
    clean_pubsub()
    clean_functions()
