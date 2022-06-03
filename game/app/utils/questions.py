from random import randrange


def get_data(game):
    data = game.db.collection('questions').document(
        game.parameter).get().to_dict()
    url = data['url']
    questions_answers = data['questions_answers']
    return url, questions_answers


def select(questions_answers, number=None):
    assert len(questions_answers) % 2 == 0
    max_number = len(questions_answers)//2
    if number is None:
        number = randrange(1, max_number + 1)
    assert number in range(1, max_number + 1)
    question = questions_answers[2*number-2]
    answer = questions_answers[2*number-1]
    return max_number, number, question, answer
