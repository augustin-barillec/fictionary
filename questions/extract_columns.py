import pandas


def extract_columns(questions_dataframe):
    questions = []
    answers = []
    sources = []
    sorted_df = questions_dataframe.sort_values(by='question')
    for row in sorted_df.to_dict(orient='records'):
        question = row['question']
        answer = row['answer']
        source = row['source']
        assert not pandas.isnull(question)
        assert not pandas.isnull(answer)
        assert not pandas.isnull(source)
        questions.append(question)
        answers.append(answer)
        sources.append(source)
    return questions, answers, sources
