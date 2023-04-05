def compute_remaining_potential_voters(potential_voters, voters):
    res = {pv: potential_voters[pv]
           for pv in potential_voters
           if pv not in voters}
    return res


def sort_users(users):
    user_ids = sorted(users, key=lambda k: users[k][0])
    return user_ids


def user_display(user_id):
    return f'<@{user_id}>'


def users_display(user_ids):
    return ' '.join([user_display(id_) for id_ in user_ids])
