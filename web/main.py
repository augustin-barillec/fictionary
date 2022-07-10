import os
import time
import logging
import google.cloud.firestore
import tools
from uuid import uuid4
from flask import Flask, request, render_template, make_response
from slack_sdk.web import WebClient
from slack_sdk.oauth import AuthorizeUrlGenerator
from reusable import secret_manager

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

project_id = os.getenv('PROJECT_ID')

db = google.cloud.firestore.Client(project=project_id)

conf = secret_manager.access_payload_parsed(
    project_id, 'distribution_conf')
slack_client_id = conf['slack_client_id']
slack_client_secret = conf['slack_client_secret']
slack_scopes = [
    'commands',
    'chat:write',
    'channels:read',
    'groups:read',
    'im:read',
    'mpim:read']

app = Flask(__name__)

authorize_url_generator = AuthorizeUrlGenerator(
    client_id=slack_client_id,
    scopes=slack_scopes)


@app.route('/')
def home():
    installation_state = str(uuid4())
    tools.firestore.store_installation_state(db, installation_state)
    url = authorize_url_generator.generate(installation_state)
    return render_template('home.html', url=url)


@app.route('/oauth/callback')
def oauth_callback():
    if 'code' not in request.args:
        error = request.args['error'] if 'error' in request.args else ''
        return make_response(
            f'Something is wrong with the installation (error: {error})', 400)
    code = request.args['code']

    installation_state = request.args['state']
    installation_state_dict = tools.firestore.consume_installation_state(
        db, installation_state)
    still_valid = False
    if installation_state_dict is not None and 'ts' in installation_state_dict:
        created = installation_state_dict['ts']
        expiration = created + 500
        still_valid = time.time() < expiration
    if not still_valid:
        return make_response(
            'Try the installation again (the state value is already expired)',
            400)

    client = WebClient()
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
        'max_running_games': 3,
        'max_running_games_per_organizer': 1,
        'refresh_interval': 4,
        'self_trigger_threshold': 60,
        'tagging': False,
        'time_to_guess_options': [300, 600, 900, 1200],
        'time_to_vote': 600
    }

    tools.firestore.store_installation(db, team_id, installation_dict)

    return 'Thank you for installing the app'


@app.route('/questions/<language>')
def qas_(language):
    qas = db.collection('qas').document(
        language).get().to_dict()['content']
    len_qas = len(qas)
    return render_template(
        'qas.html',
        capitalized_language=language.capitalize(),
        len_qas=len_qas,
        qas=qas)


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


if __name__ == "__main__":
    app.run(debug=True, port=5100)
