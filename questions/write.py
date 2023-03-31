import argparse
import google.cloud.firestore
import pandas
import extract_columns
parser = argparse.ArgumentParser()
parser.add_argument('project_id')
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)


def read_tsv(basename):
    return pandas.read_csv(basename, sep='\t')


questions_dataframes = dict()
questions_dataframes['English'] = read_tsv('questions - English.tsv')
questions_dataframes['French'] = read_tsv('questions - French.tsv')
for language in ['English', 'French']:
    questions_dataframe = questions_dataframes[language]
    questions, answers, sources = extract_columns.extract_columns(
        questions_dataframe)
    data = {
        'questions': questions,
        'answers': answers,
        'sources': sources}
    db.collection('questions').document(language).set(data, merge=False)
