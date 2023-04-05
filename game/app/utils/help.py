import app.utils as ut


def build_msg(game):
    home_url = ut.firestore.get_home_url(game.db)
    msg = ut.text.This_is_an_app_for_Slack[game.language].format(
        home_url=home_url)
    return msg
