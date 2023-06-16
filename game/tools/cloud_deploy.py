import logging
import subprocess
import time
import tools
logger = logging.getLogger(__name__)


def deploy_pubsub(project_id):
    import google.cloud.pubsub_v1
    port_to_function_name = tools.ports.port_to_function_name
    port_to_signature_type = tools.ports.port_to_signature_type
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


def deploy_function(project_id, region, port, pre_sleep_duration):
    logger.info(f'Pre-sleeping {pre_sleep_duration}s...')
    time.sleep(pre_sleep_duration)
    logger.info(f'Pre-slept {pre_sleep_duration}s')
    command_template = """
    gcloud functions deploy {function_name} \
    --project {project_id} \
    --region {region} \
    --docker-registry artifact-registry \
    --runtime python311 \
    --timeout 540s \
    --trigger-{trigger_type} {min_instances} {security_level} \
    --set-env-vars PROJECT_ID={project_id} 2>&1 | tee {filepath}
    """
    function_name = tools.ports.port_to_function_name[port]
    signature_type = tools.ports.port_to_signature_type[port]
    assert signature_type in ('http', 'event')
    if signature_type == 'http':
        trigger_type = 'http'
        min_instances = '--min-instances 1'
        security_level = '--security-level secure-always'
    else:
        topic_name = tools.pubsub_names.topic.format(
            function_name=function_name)
        trigger_type = f'topic {topic_name}'
        min_instances = ''
        security_level = ''
    filepath = tools.local_paths.cloud_deploy_function_file.format(port=port)
    command = command_template.format(
        function_name=function_name,
        project_id=project_id,
        region=region,
        trigger_type=trigger_type,
        min_instances=min_instances,
        security_level=security_level,
        filepath=filepath)
    subprocess.run(command, shell=True)
    with open(filepath) as f:
        assert 'done' in f.read()
        logger.info(f'port={port} successfully deployed')
