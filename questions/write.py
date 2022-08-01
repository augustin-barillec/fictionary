import argparse
import google.cloud.firestore
import questions_answers
parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)
for language in ['english', 'french']:
    qas = getattr(questions_answers, f'questions_answers_{language}')
    assert len(qas) % 2 == 0
    data = {'questions_answers': qas}
    db.collection('questions').document(language).set(data, merge=True)
