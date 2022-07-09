def get_url(game):
    url = game.db.collection('url').document('url').get().to_dict()['url']
    return url
