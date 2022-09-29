import argparse
import pandas
import google.cloud.firestore
import extract_columns

parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)
questions_dataframe = pandas.read_csv(
    'questions - Sheet1.tsv', sep='\t')

for language in ['english', 'french']:
    questions, answers, sources, credits_ = extract_columns.extract_columns(
        language, questions_dataframe)
    data = {
        'questions': questions,
        'answers': answers,
        'sources': sources,
        'credits': credits_}
    db.collection('questions').document(language).set(data, merge=False)
