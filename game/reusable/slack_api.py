def crashable(api_call):
    def decored(*args):
        resp = api_call(*args)
        if 'ok' in resp and resp['ok']:
            return resp
        else:
            raise RuntimeError(resp)
    return decored


@crashable
def conversations_info(slack_client, channel_id):
    return slack_client.api_call(
        'conversations.info', channel=channel_id, include_num_members=True)


@crashable
def chat_postmessage(slack_client, channel_id, blocks):
    return slack_client.api_call(
        'chat.postMessage',
        channel=channel_id,
        blocks=blocks)


def chat_postephemeral(slack_client, channel_id, user_id, msg):
    return slack_client.api_call(
        'chat.postEphemeral',
        channel=channel_id,
        user=user_id,
        text=msg)


@crashable
def chat_update(slack_client, channel_id, blocks, ts):
    return slack_client.api_call(
        'chat.update',
        channel=channel_id,
        blocks=blocks,
        ts=ts)


@crashable
def views_open(slack_client, trigger_id, view):
    return slack_client.api_call(
        'views.open',
        trigger_id=trigger_id,
        view=view)


@crashable
def views_update(slack_client, view_id, view):
    return slack_client.api_call(
        'views.update',
        view_id=view_id,
        view=view)


@crashable
def views_push(slack_client, trigger_id, view):
    return slack_client.api_call(
        'views.push',
        trigger_id=trigger_id,
        view=view)
