import logging
import os
import flask
import google.cloud.firestore
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger()
project_id = os.getenv('PROJECT_ID')
db = google.cloud.firestore.Client(project=project_id)
app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/questions_<language>')
def questions_(language):
    questions_dict = db.collection('questions').document(
        language).get().to_dict()
    questions = questions_dict['questions']
    answers = questions_dict['answers']
    sources = questions_dict['sources']
    return flask.render_template(
        'questions.html',
        capitalized_language=language.capitalize(),
        len_questions=len(questions),
        questions=questions,
        answers=answers,
        sources=sources)


@app.route('/privacy_policy')
def privacy_policy():
    return flask.render_template('privacy_policy.html')


if __name__ == "__main__":
    app.run(debug=True, port=5100)
