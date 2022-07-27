import os
import logging
import google.cloud.firestore
from flask import Flask, render_template


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
project_id = os.getenv('PROJECT_ID')
db = google.cloud.firestore.Client(project=project_id)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/questions/<language>')
def questions_answers_(language):
    questions_answers = db.collection('questions').document(
        language).get().to_dict()['questions_answers']
    len_questions_answers = len(questions_answers)
    return render_template(
        'questions_answers.html',
        capitalized_language=language.capitalize(),
        len_qas=len_questions_answers,
        qas=questions_answers)


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


if __name__ == "__main__":
    app.run(debug=True, port=5100)
