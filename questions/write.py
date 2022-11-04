import argparse
import pandas
import google.cloud.firestore
import extract_columns

parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)


def read_tsv(basename):
    return pandas.read_csv(basename, sep='\t')


questions_dataframes = dict()
questions_dataframes['english'] = read_tsv('questions - english.tsv')
questions_dataframes['french'] = read_tsv('questions - french.tsv')


for language in ['english', 'french']:
    questions_dataframe = questions_dataframes[language]
    questions, answers, sources = extract_columns.extract_columns(
        questions_dataframe)
    data = {
        'questions': questions,
        'answers': answers,
        'sources': sources}
    db.collection('questions').document(language).set(data, merge=False)
