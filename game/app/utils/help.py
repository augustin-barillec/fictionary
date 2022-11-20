import app.utils as ut


def build_msg(game):
    home_url = ut.firestore.get_home_url(game.db)
    msg = ('This is a slack app to play fictionary. '
           f'All information is available <{home_url}|here.>')
    return msg
