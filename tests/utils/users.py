def get_user_ids(conf):
    res = []
    for user in conf['users']:
        user_id = user['id']
        res.append(user_id)
    return res
