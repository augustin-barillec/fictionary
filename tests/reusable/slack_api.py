def conversations_list(slack_client):
    return slack_client.conversations_list()


def conversations_create(slack_client, channel_name):
    return slack_client.conversations_create(name=channel_name)


def conversations_members(slack_client, channel_id):
    return slack_client.conversations_members(channel=channel_id)


def conversations_invite(slack_client, channel_id, user_id):
    return slack_client.conversations_invite(channel=channel_id, users=user_id)


def conversations_join(slack_client, channel_id):
    return slack_client.conversations_join(channel=channel_id)


def conversations_kick(slack_client, channel_id, user_id):
    return slack_client.conversations_kick(channel=channel_id, user=user_id)


def conversations_leave(slack_client, channel_id):
    return slack_client.conversations_leave(channel=channel_id)
