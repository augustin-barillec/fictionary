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
project_id = os.getenv('PROJECT_ID')
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
    url = authorize_url_generator.generate(installation_state)
    return flask.render_template('home.html', url=url)


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
    if installation_state_dict is not None and 'ts' in installation_state_dict:
        created = installation_state_dict['ts']
        expiration = created + 500
        still_valid = time.time() < expiration
    if not still_valid:
        return flask.render_template('try_again.html'), 400

    client = slack_sdk.web.WebClient()
    oauth_response = client.oauth_v2_access(
        client_id=slack_client_id,
        client_secret=slack_client_secret,
        code=code)
    installed_team = oauth_response.get('team', {})
    installer = oauth_response.get('authed_user', {})
    bot_token = oauth_response.get('access_token')
    bot_id = None
    if bot_token is not None:
        auth_test = client.auth_test(token=bot_token)
        bot_id = auth_test['bot_id']
    app_id = oauth_response.get('app_id')
    team_id = installed_team.get('id')
    team_name = installed_team.get('name')
    bot_token = bot_token
    bot_id = bot_id
    bot_user_id = oauth_response.get('bot_user_id')
    bot_scopes = oauth_response.get('scope')
    user_id = installer.get('id')
    token_type = oauth_response.get('token_type')

    installation_dict = {
        'app_id': app_id,
        'bot_id': bot_id,
        'bot_scopes': bot_scopes,
        'slack_token': bot_token,
        'bot_user_id': bot_user_id,
        'team_name': team_name,
        'token_type': token_type,
        'user_id': user_id,

        'max_guessers_per_game': 20,
        'max_life_span': 3600,
        'max_running_games': 5,
        'max_running_games_per_organizer': 1,
        'refresh_interval': 4,
        'self_trigger_threshold': 60,
        'tagging': False,
        'time_to_guess': 900,
        'time_to_vote': 300,
        'trigger_cooldown': 30}
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
