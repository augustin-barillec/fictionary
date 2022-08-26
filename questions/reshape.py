import pandas


def extract_questions_answers_couples(language, questions_answers_dataframe):
    res = []
    for row in questions_answers_dataframe.to_dict(orient='records'):
        question = row[f'{language}_question']
        answer = row[f'{language}_answer']
        if pandas.isnull(question):
            assert pandas.isnull(answer)
            continue
        res.append((question, answer))
    return res


def build_questions_answers_list(questions_answers_couples):
    res = []
    for question, answer in questions_answers_couples:
        res.append(question)
        res.append(answer)
    return res
