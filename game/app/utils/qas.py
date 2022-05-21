from random import randrange


def get_qas(game):
    res = game.db.collection('qas').document(
        game.parameter).get().to_dict()['content']
    return res


def select(qas, number=None):
    assert len(qas) % 2 == 0
    max_number = len(qas)//2
    if number is None:
        number = randrange(1, max_number + 1)
    assert number in range(1, max_number + 1)
    q = qas[2*number-2]
    a = qas[2*number-1]
    return max_number, number, q, a
