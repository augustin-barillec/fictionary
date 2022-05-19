import os
import subprocess
from reusable import publisher, subscriber
from tools import local_clean, local_paths, ports, pubsub_names


PUBSUB_EMULATOR_HOST = '0.0.0.0:8085'


def deploy_pubsub(project_id):
    local_clean.clean_pubsub()
    port_to_function_name = ports.port_to_function_name
    port_to_signature_type = ports.port_to_signature_type
    data_dir_path = local_paths.pubsub_data_dir
    command = f"""
    gcloud beta emulators pubsub start \
    --project={project_id} \
    --data-dir={data_dir_path} \
    --host-port={PUBSUB_EMULATOR_HOST} &
    """
    subprocess.run(command, shell=True)
    os.environ['PUBSUB_EMULATOR_HOST'] = PUBSUB_EMULATOR_HOST
    for port in ports.ports:
        function_name = port_to_function_name[port]
        signature_type = port_to_signature_type[port]
        if signature_type == 'event':
            topic_name = pubsub_names.topic.format(function_name=function_name)
            subscription_name = pubsub_names.sub.format(
                function_name=function_name)
            endpoint = f'http://0.0.0.0:{port}'
            publisher.create_topic(project_id, topic_name)
            subscriber.create_push_subscription(
                project_id,
                topic_name,
                subscription_name,
                endpoint)


def deploy_functions(project_id):
    local_clean.clean_functions()
    os.environ['PROJECT_ID'] = project_id
    os.environ['PUBSUB_PROJECT_ID'] = project_id
    os.environ['PUBSUB_EMULATOR_HOST'] = PUBSUB_EMULATOR_HOST
    command_template = """
    functions-framework \
    --target {function_name} \
    --port {port} \
    --signature-type {signature_type} \
    > {filepath} 2>&1 &
    """
    for port in ports.ports:
        function_name = ports.port_to_function_name[port]
        signature_type = ports.port_to_signature_type[port]
        filepath = local_paths.local_function_file.format(port=port)
        command = command_template.format(
            function_name=function_name,
            port=port,
            signature_type=signature_type,
            filepath=filepath)
        subprocess.run(command, shell=True)
