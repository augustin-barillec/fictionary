import argparse
import google.cloud.firestore
import questions_answers
parser = argparse.ArgumentParser()
parser.add_argument('--project_id', required=True)
args = parser.parse_args()
db = google.cloud.firestore.Client(project=args.project_id)
for language in ['english', 'french']:
    data = {'questions_answers': getattr(
        questions_answers, f'questions_answers_{language}')}
    db.collection('questions').document(language).set(data, merge=True)
