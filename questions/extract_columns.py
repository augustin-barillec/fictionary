import pandas


def extract_columns(language, questions_dataframe):
    questions = []
    answers = []
    sources = []
    credits_ = []
    col_question = f'{language}_question'
    col_answer = f'{language}_answer'
    sorted_df = questions_dataframe.sort_values(by=col_question)
    for row in sorted_df.to_dict(orient='records'):
        question = row[col_question]
        answer = row[col_answer]
        source = row['source']
        credit = row['credit']
        if pandas.isnull(question):
            assert pandas.isnull(answer)
            continue
        assert not pandas.isnull(source)
        if pandas.isnull(credit):
            credit = ''
        questions.append(question)
        answers.append(answer)
        sources.append(source)
        credits_.append(credit)
    return questions, answers, sources, credits_
