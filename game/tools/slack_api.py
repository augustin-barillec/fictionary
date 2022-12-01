def auth_test(slack_client):
    return slack_client.auth_test()


def chat_postmessage(slack_client, channel_id, blocks):
    return slack_client.chat_postMessage(
        channel=channel_id,
        blocks=blocks)


def chat_postephemeral(slack_client, channel_id, user_id, msg):
    return slack_client.chat_postEphemeral(
        channel=channel_id,
        user=user_id,
        text=msg)


def chat_update(slack_client, channel_id, blocks, ts):
    return slack_client.chat_update(
        channel=channel_id,
        blocks=blocks,
        ts=ts)


def views_open(slack_client, trigger_id, view):
    return slack_client.views_open(
        trigger_id=trigger_id,
        view=view)


def views_update(slack_client, view_id, view):
    return slack_client.views_update(
        view_id=view_id,
        view=view)


def views_push(slack_client, trigger_id, view):
    return slack_client.views_push(
        trigger_id=trigger_id,
        view=view)
