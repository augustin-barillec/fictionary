import time


def store_installation_state(db, installation_state):
    state_ref = db.collection('installation_states').document(
        installation_state)
    ts = time.time()
    ts_to_expire = ts + 3600
    state_ref.set({'ts': ts, 'ts_to_expire': ts_to_expire}, merge=False)


def consume_installation_state(db, installation_state):
    state_ref = db.collection('installation_states').document(
        installation_state)
    state_dict = state_ref.get().to_dict()
    state_ref.delete()
    return state_dict


def store_installation(db, team_id, installation_dict):
    team_ref = db.collection('teams').document(team_id)
    team_ref.set(installation_dict, merge=False)
