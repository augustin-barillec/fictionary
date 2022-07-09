from app.utils import url


def build_msg(game):
    url_ = url.get_url(game)
    msg = ('This is a slack app to play fictionary. '
           f'All infos are available <{url_}|here.>')
    return msg
