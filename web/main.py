import os
import time
import uuid
import flask
import google.cloud.firestore
import slack_sdk.oauth
import slack_sdk.web
import reusable
import tools
logger = reusable.root_logger.configure_root_logger()
app = flask.Flask(__name__)
project_id = os.environ['PROJECT_ID']
db = google.cloud.firestore.Client(project=project_id)
oauth_credentials = reusable.secret_manager.access_payload_parsed(
    project_id, 'oauth_credentials')
slack_client_id = oauth_credentials['slack_client_id']
slack_client_secret = oauth_credentials['slack_client_secret']
slack_scopes = ['commands', 'chat:write']
authorize_url_generator = slack_sdk.oauth.AuthorizeUrlGenerator(
    client_id=slack_client_id,
    scopes=slack_scopes)


@app.route('/')
def home():
    installation_state = str(uuid.uuid4())
    tools.firestore.store_installation_state(db, installation_state)
    return flask.render_template(
        'home.html',
        installation_state=installation_state)


@app.route('/language_<language>_<installation_state>')
def version(language, installation_state):
    tools.firestore.add_language_to_installation_state(
        db, installation_state, language)
    url = authorize_url_generator.generate(installation_state)
    return flask.redirect(url)


@app.route('/oauth_callback')
def oauth_callback():
    if 'code' not in flask.request.args:
        error = flask.request.args['error'] \
            if 'error' in flask.request.args else ''
        msg = f'Something is wrong with the installation (error: {error})'
        return flask.make_response(msg, 400)
    code = flask.request.args['code']

    installation_state = flask.request.args['state']
    installation_state_dict = tools.firestore.consume_installation_state(
        db, installation_state)

    still_valid = False
    language = None
    if installation_state_dict is not None:
        created = installation_state_dict['ts']
        language = installation_state_dict['language']
        expiration = created + 500
        still_valid = time.time() < expiration
    if not still_valid:
        return flask.render_template('try_again.html'), 400

    assert language in ('English', 'French')

    client = slack_sdk.web.WebClient()
    oauth_response = client.oauth_v2_access(
        client_id=slack_client_id,
        client_secret=slack_client_secret,
        code=code)
    installed_team = oauth_response.get('team', {})
    team_id = installed_team.get('id')
    bot_token = oauth_response.get('access_token')
    app_id = oauth_response.get('app_id')
    bot_scopes = oauth_response.get('scope')
    token_type = oauth_response.get('token_type')

    installation_dict = {
        'app_id': app_id,
        'bot_scopes': bot_scopes,
        'language': language,
        'slack_token': bot_token,
        'token_type': token_type}
    installation_dict = {
        **installation_dict, **reusable.game_params.game_params}
    tools.firestore.store_installation(db, team_id, installation_dict)
    return flask.render_template('thank_you.html')


@app.route('/questions_<language>')
def questions_(language):
    questions_dict = db.collection('questions').document(
        language).get().to_dict()
    questions = questions_dict['questions']
    answers = questions_dict['answers']
    sources = questions_dict['sources']
    return flask.render_template(
        'questions.html',
        language=language,
        len_questions=len(questions),
        questions=questions,
        answers=answers,
        sources=sources)


@app.route('/privacy_policy')
def privacy_policy():
    return flask.render_template('privacy_policy.html')


@app.route('/terms_of_service')
def terms_of_service():
    return flask.render_template('terms_of_service.html')


if __name__ == "__main__":
    app.run(debug=True, port=5100)
