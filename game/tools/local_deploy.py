import os
import subprocess
import logging
import tools
logger = logging.getLogger(__name__)
PUBSUB_EMULATOR_HOST = '0.0.0.0:8085'


def deploy_pubsub(project_id):
    import google.cloud.pubsub_v1
    tools.local_clean.clean_pubsub()
    data_dir_path = tools.local_paths.pubsub_data_dir
    os.makedirs(data_dir_path)
    port_to_function_name = tools.ports.port_to_function_name
    port_to_signature_type = tools.ports.port_to_signature_type
    data_dir_path = tools.local_paths.pubsub_data_dir
    command = f"""
    gcloud beta emulators pubsub start \
    --project={project_id} \
    --data-dir={data_dir_path} \
    --host-port={PUBSUB_EMULATOR_HOST} &
    """
    subprocess.run(command, shell=True)
    os.environ['PUBSUB_EMULATOR_HOST'] = PUBSUB_EMULATOR_HOST
    for port in tools.ports.ports:
        function_name = port_to_function_name[port]
        signature_type = port_to_signature_type[port]
        if signature_type == 'event':
            publisher = google.cloud.pubsub_v1.PublisherClient()
            topic_name = tools.pubsub_names.topic.format(
                function_name=function_name)
            topic_path = publisher.topic_path(project_id, topic_name)
            topic = publisher.create_topic(request={'name': topic_path})
            logger.info(f'Created topic: {topic.name}')
            subscriber = google.cloud.pubsub_v1.SubscriberClient()
            subscription_name = tools.pubsub_names.sub.format(
                function_name=function_name)
            subscription_path = subscriber.subscription_path(
                project_id, subscription_name)
            endpoint = f'http://0.0.0.0:{port}'
            push_config = google.cloud.pubsub_v1.types.PushConfig(
                push_endpoint=endpoint)
            with subscriber:
                subscription = subscriber.create_subscription(
                    request={
                        'name': subscription_path,
                        'topic': topic_path,
                        'push_config': push_config})
            logger.info(f'Push subscription created: {subscription}')
            logger.info(f'Endpoint for subscription is: {endpoint}')


def deploy_functions(project_id):
    tools.local_clean.clean_functions()
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
    for port in tools.ports.ports:
        function_name = tools.ports.port_to_function_name[port]
        signature_type = tools.ports.port_to_signature_type[port]
        filepath = tools.local_paths.local_function_file.format(port=port)
        command = command_template.format(
            function_name=function_name,
            port=port,
            signature_type=signature_type,
            filepath=filepath)
        subprocess.run(command, shell=True)
