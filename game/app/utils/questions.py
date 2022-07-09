from random import randrange
from app.utils import url


def get_questions_url(game):
    res = url.get_url(game)
    res = f'{res}/questions/{game.parameter}'
    return res


def get_questions_answers(game):
    res = game.db.collection('questions').document(
        game.parameter).get().to_dict()['questions_answers']
    return res


def select(questions_answers, number=None):
    assert len(questions_answers) % 2 == 0
    max_number = len(questions_answers)//2
    if number is None:
        number = randrange(1, max_number + 1)
    assert number in range(1, max_number + 1)
    question = questions_answers[2*number-2]
    answer = questions_answers[2*number-1]
    return max_number, number, question, answer
