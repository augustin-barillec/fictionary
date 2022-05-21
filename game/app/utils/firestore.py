import reusable
from app.utils import ids


class FirestoreReader:
    def __init__(self, db, game_id):
        self.db = db
        self.game_id = game_id
        self.team_id = ids.game_id_to_team_id(self.game_id)
        self.channel_id = ids.game_id_to_channel_id(self.game_id)

    def get_team_ref(self):
        return self.db.collection('teams').document(self.team_id)

    def get_channels_ref(self):
        return self.get_team_ref().collection('channels')

    def get_games_ref(self):
        return self.get_team_ref().collection('games')

    def get_channel_ref(self):
        return self.get_channels_ref().document(self.channel_id)

    def get_game_ref(self):
        return self.get_games_ref().document(self.game_id)

    def get_team_dict(self):
        team_ref = self.get_team_ref()
        return team_ref.get().to_dict()

    def get_channel_dict(self):
        return self.get_channel_ref().get().to_dict()

    def get_game_dict(self):
        return self.get_game_ref().get().to_dict()

    def get_channel_dicts(self):
        return reusable.firestore.get_dicts(self.get_channels_ref())

    def get_game_dicts(self):
        return reusable.firestore.get_dicts(self.get_games_ref())


class FirestoreEditor:

    def __init__(self, game):
        self.game = game

    def set_game(self, merge):
        self.game.ref.set(self.game.dict, merge=merge)
