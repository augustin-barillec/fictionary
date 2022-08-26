import argparse
import pandas
import google.cloud.firestore
import reshape

parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)
questions_answers_dataframe = pandas.read_csv(
    'questions_answers - Sheet1.tsv', sep='\t')

for language in ['english', 'french']:
    qas_couples = reshape.extract_questions_answers_couples(
        language, questions_answers_dataframe)
    qas_couples = sorted(qas_couples)
    qas_list = reshape.build_questions_answers_list(qas_couples)
    assert len(qas_list) % 2 == 0
    data = {'questions_answers': qas_list}
    db.collection('questions').document(language).set(data, merge=False)
