import time


def store_installation_state(db, installation_state):
    state_ref = db.collection('installation_states').document(
        installation_state)
    now = time.time()
    state_ref.set({'ts': now}, merge=False)


def consume_installation_state(db, installation_state):
    state_ref = db.collection('installation_states').document(
        installation_state)
    state_dict = state_ref.get().to_dict()
    state_ref.delete()
    return state_dict


def store_installation(db, team_id, installation_dict):
    team_ref = db.collection('teams').document(team_id)
    team_ref.set(installation_dict, merge=False)
