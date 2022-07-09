import subprocess
from tools import ports, local_paths, pubsub_names


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
            print(f'Created topic: {topic.name}')


def deploy_function(project_id, region, port):
    command_template = """
    gcloud functions deploy {function_name} \
    --project {project_id} \
    --region {region} \
    --runtime python310 \
    --timeout 540s \
    --ignore-file .functionsignore \
    --trigger-{trigger_type} {allow_unauthenticated} {min_instances} \
    --set-env-vars PROJECT_ID={project_id} 2>&1 | tee {filepath}
    """
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
        filepath=filepath)
    subprocess.run(command, shell=True)
    with open(filepath) as f:
        assert 'done' in f.read()
        print(f'port={port} successfully deployed')
