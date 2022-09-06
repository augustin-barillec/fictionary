import subprocess
import time
import logging
from tools import ports, local_paths, pubsub_names

logger = logging.getLogger(__name__)


def deploy_pubsub(project_id):
    from google.cloud import pubsub_v1
    port_to_function_name = ports.port_to_function_name
    port_to_signature_type = ports.port_to_signature_type
    for port in ports.ports:
        function_name = port_to_function_name[port]
        signature_type = port_to_signature_type[port]
        if signature_type == 'event':
            publisher = pubsub_v1.PublisherClient()
            topic_name = pubsub_names.topic.format(function_name=function_name)
            topic_path = publisher.topic_path(project_id, topic_name)
            topic = publisher.create_topic(request={'name': topic_path})
            logger.info(f'Created topic: {topic.name}')


def deploy_function(project_id, region, port, pre_sleep_duration):
    logger.info(f'Pre-sleeping {pre_sleep_duration}s...')
    time.sleep(pre_sleep_duration)
    logger.info(f'Pre-slept {pre_sleep_duration}s')
    command_template = """
    gcloud functions deploy {function_name} \
    --project {project_id} \
    --region {region} \
    --docker-registry artifact-registry \
    --runtime python310 \
    --timeout 540s \
    --ignore-file .functionsignore \
    --trigger-{trigger_type} {min_instances} \
    --set-env-vars PROJECT_ID={project_id} 2>&1 | tee {filepath}
    """
    function_name = ports.port_to_function_name[port]
    signature_type = ports.port_to_signature_type[port]
    assert signature_type in ('http', 'event')
    if signature_type == 'http':
        trigger_type = 'http'
        min_instances = '--min-instances 1'
    else:
        topic_name = pubsub_names.topic.format(function_name=function_name)
        trigger_type = f'topic {topic_name}'
        min_instances = ''
    filepath = local_paths.cloud_deploy_function_file.format(port=port)
    command = command_template.format(
        function_name=function_name,
        project_id=project_id,
        region=region,
        trigger_type=trigger_type,
        min_instances=min_instances,
        filepath=filepath)
    subprocess.run(command, shell=True)
    with open(filepath) as f:
        assert 'done' in f.read()
        logger.info(f'port={port} successfully deployed')
