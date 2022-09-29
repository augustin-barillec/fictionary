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


@app.route('/questions_<language>')
def questions_(language):
    questions_dict = db.collection('questions').document(
        language).get().to_dict()
    questions = questions_dict['questions']
    answers = questions_dict['answers']
    sources = questions_dict['sources']
    credits_ = questions_dict['credits']
    return render_template(
        'questions.html',
        capitalized_language=language.capitalize(),
        len_questions=len(questions),
        questions=questions,
        answers=answers,
        sources=sources,
        credits_=credits_)


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


if __name__ == "__main__":
    app.run(debug=True, port=5100)
