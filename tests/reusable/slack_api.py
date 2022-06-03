def crashable(api_call):
    def decored(*args):
        resp = api_call(*args)
        if 'ok' in resp and resp['ok']:
            return resp
        else:
            raise RuntimeError(resp)
    return decored


@crashable
def conversations_list(slack_client):
    return slack_client.api_call('conversations.list')


@crashable
def conversations_create(slack_client, channel_name):
    return slack_client.api_call(
        'conversations.create',
        name=channel_name)


@crashable
def conversations_members(slack_client, channel_id):
    return slack_client.api_call(
        'conversations.members',
        channel=channel_id)


@crashable
def conversations_invite(slack_client, channel_id, user_id):
    return slack_client.api_call(
        'conversations.invite',
        channel=channel_id,
        users=user_id)


@crashable
def conversations_join(slack_client, channel_id):
    return slack_client.api_call(
        'conversations.join',
        channel=channel_id)


@crashable
def conversations_kick(slack_client, channel_id, user_id):
    return slack_client.api_call(
        'conversations.kick',
        channel=channel_id,
        user=user_id)


@crashable
def conversations_leave(slack_client, channel_id):
    return slack_client.api_call(
        'conversations.leave',
        channel=channel_id)
