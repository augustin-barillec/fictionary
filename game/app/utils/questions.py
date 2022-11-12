import random
import app.utils as ut


def get_questions_url(game):
    home_url = ut.firestore.get_home_url(game.db)
    return f'{home_url}/questions_{game.parameter}'


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
        number = random.randrange(1, max_number + 1)
    assert number in range(1, max_number + 1)
    question = questions[number - 1]
    answer = answers[number - 1]
    return number, question, answer
