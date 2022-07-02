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
    return slack_client.conversations_info(
        channel=channel_id, include_num_members=True)


@crashable
def chat_postmessage(slack_client, channel_id, blocks):
    return slack_client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text='error')


def chat_postephemeral(slack_client, channel_id, user_id, msg):
    return slack_client.chat_postEphemeral(
        channel=channel_id,
        user=user_id,
        text=msg)


@crashable
def chat_update(slack_client, channel_id, blocks, ts):
    return slack_client.chat_update(
        channel=channel_id,
        blocks=blocks,
        ts=ts,
        text='error')


@crashable
def views_open(slack_client, trigger_id, view):
    return slack_client.views_open(
        trigger_id=trigger_id,
        view=view)


@crashable
def views_update(slack_client, view_id, view):
    return slack_client.views_update(
        view_id=view_id,
        view=view)


@crashable
def views_push(slack_client, trigger_id, view):
    return slack_client.views_push(
        trigger_id=trigger_id,
        view=view)
