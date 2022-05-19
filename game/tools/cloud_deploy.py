import subprocess
import logging
import time
import reusable
from tools import ports, local_paths, pubsub_names

logger = logging.getLogger(__name__)


def deploy_pubsub(project_id):
    port_to_function_name = ports.port_to_function_name
    port_to_signature_type = ports.port_to_signature_type
    for port in ports.ports:
        function_name = port_to_function_name[port]
        signature_type = port_to_signature_type[port]
        if signature_type == 'event':
            topic_name = pubsub_names.topic.format(function_name=function_name)
            reusable.publisher.create_topic(project_id, topic_name)


def deploy_functions(
        project_id, region, single_port=None, pre_sleep_duration=None):
    if pre_sleep_duration is not None:
        logger.info(f'Pre-sleeping {pre_sleep_duration}s...')
        time.sleep(pre_sleep_duration)
        logger.info(f'Pre-slept {pre_sleep_duration}s')
    command_template = """
    gcloud alpha functions deploy {function_name} \
    --project {project_id} \
    --region {region} \
    --runtime python39 \
    --timeout 540s \
    --ignore-file .functionsignore \
    --trigger-{trigger_type} {allow_unauthenticated} {min_instances} \
    --set-env-vars PROJECT_ID={project_id} 2>&1 | tee {filepath} {background}
    """
    if single_port is not None:
        assert single_port in ports.ports
        ports_to_deploy = [single_port]
        background = ''
    else:
        ports_to_deploy = ports.ports
        background = '&'
    for port in ports_to_deploy:
        function_name = ports.port_to_function_name[port]
        signature_type = ports.port_to_signature_type[port]
        assert signature_type in ('http', 'event')
        if signature_type == 'http':
            trigger_type = 'http'
            allow_unauthenticated = '--allow-unauthenticated'
            min_instances = '--min-instances 1'
        else:
            topic_name = pubsub_names.topic.format(function_name=function_name)
            trigger_type = f'topic {topic_name}'
            allow_unauthenticated = ''
            min_instances = ''
        filepath = local_paths.cloud_deploy_function_file.format(port=port)
        command = command_template.format(
            function_name=function_name,
            project_id=project_id,
            region=region,
            trigger_type=trigger_type,
            allow_unauthenticated=allow_unauthenticated,
            min_instances=min_instances,
            filepath=filepath,
            background=background)
        subprocess.run(command, shell=True)
        if single_port is not None:
            with open(filepath) as f:
                assert 'done' in f.read()
                logger.info(f'port={single_port} successfully deployed')
