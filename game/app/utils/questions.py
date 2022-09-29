from random import randrange
from app.utils import url


def get_questions_url(game):
    res = url.get_url(game)
    res = f'{res}/questions_{game.parameter}'
    return res


def get_questions_answers(game):
    questions_dict = game.db.collection('questions').document(
        game.parameter).get().to_dict()
    questions = questions_dict['questions']
    answers = questions_dict['answers']
    assert len(questions) == len(answers)
    return questions, answers


def select(questions, answers, number=None):
    max_number = len(questions)
    if number is None:
        number = randrange(1, max_number + 1)
    assert number in range(1, max_number + 1)
    question = questions[number - 1]
    answer = answers[number - 1]
    return number, question, answer
