# Fictionary

Fictionary is a Slack app to play [fictionary](https://en.wikipedia.org/wiki/Fictionary).

This app runs on a single GCP project_id.

## Links

- Website: https://yokyok.ninja
- Demo: https://www.youtube.com/watch?v=QCxpt5dB5KU
- Source code: https://github.com/augustin-barillec/fictionary

## Structure

This project has five directories:

- cloudbuild
- game
- questions
- tests
- web

The questions directory contains the questions of the game and a script to 
write them to Firestore.

The web directory contains the code for the app website.

The game directory contains the code which runs the Fictionary games. The 
entry point is the main.py file containing 9 Cloud Functions.

The cloudbuild directory contains 3 files. These define Cloud Build triggers 
which deploy the game, the questions and the website.

The tests directory contains Cypress code that simulates different game 
scenarios on a real Slack workspace.

## Game

The 9 Cloud Functions written in the main.py file of the game directory are 
the following:

- slash_command
- interactivity
- pre_guess_stage
- guess_stage
- pre_vote_stage
- vote_stage
- pre_result_stage
- result_stage
- clean

The slash_command and interactivity Cloud Functions are HTTP Functions. The 
others are triggered by Pub/Sub topics. 

The slash_commmand function handles the slash command "/fictionary". It has 4 
parameters: "help", "freestyle", "english" and "french". The first one displays 
information about the app. The last three open a view for the user to configure 
and start a game.

The interactivity function handles all the user interactions with Slack objects 
of a game: game setup view configuration and submission, guess button click and 
guess view submission, vote button click and vote view submission.

The clean function is triggered once a day via Cloud Scheduler. It deletes games
that were created more than one hour ago and that finished successfully from 
Firestore. It moves games that where created more than one hour ago and that 
failed in a collection named fails in Firestore to help for debugging. These 
failed games are automatically deleted about 3 days after they were moved.

The clean function sends also some monitoring information about these games 
into BigQuery (but no data written by users is sent).

Thus, data written by users in successful games (which should be the usual case) 
are kept at most about 1 day. Data written by users in failed games are kept 
about 3 days more.

Firestore contains a collection named teams containing team_ids (e.g. TXXXXXXX). 
These are the teams where the app is installed. Each team_id document has some 
global parameters for its games (for instance the parameters time_to_guess or 
max_guessers_per_game). 

Each team_id document has a collection named games. When a user sends the slash
command to set up a game, a game_id is stored in this collection and a game 
setup view is displayed to the user. When the user submits the view, 
the interactivity function triggers the pre_guess_stage function.

The latter computes the guess deadline, displays the guess button and the timer
and triggers the guess_stage function. This function is a loop which 
refreshes the timer and the names of guessers in Slack. 

The names of the guessers and the guesses are stored in Firestore in the 
game document by the interactivity function when guessers submit their guess. 

When the timer is over or the maximum numbers of guessers is reached, the
guess_stage function triggers the pre_vote_stage function. The pre_vote_stage
and the vote_stage functions work similarly than the pre_guess_stage
and the guess_stage functions. 

The pre_result_stage function computes the results and triggers the result_stage 
function which displays them. 

## Testing

First you need your own GCP project P and your own Slack workspace T. 

In the Slack workspace T, you need to create 4 users named A0, A1, A2 and A3. 

On P, you can deploy the game, the questions and the website, using the files 
in the cloudbuild directory. 

You have also to create Pub/Sub topics (one for each event-driven function). 
For this, you can run from the game directory:

```shell
python cloud_deploy.py P pubsub
```

You can create your own Fictionary Slack app in T with the following manifest:

```yaml
display_information:
  name: Fictionary
  description: An app to play fictionary!
  background_color: "#004492"
features:
  bot_user:
    display_name: Fictionary
    always_online: true
  slash_commands:
    - command: /fictionary
      url: the url of the slash_command function
      description: Start a fictionary game!
      usage_hint: "[help, freestyle, english, french]"
      should_escape: false
oauth_config:
  scopes:
    bot:
      - commands
      - chat:write
settings:
  interactivity:
    is_enabled: true
    request_url: the url of the interactivity function
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

Then you have to create a second Slack app named cypress for setting up 
channels in the workspace T. Each channel will host a specific Cypress test. 

```yaml
display_information:
  name: cypress
  description: setup channels for testing
features:
  bot_user:
    display_name: cypress
    always_online: true
oauth_config:
  scopes:
    bot:
      - channels:manage
      - channels:read
      - channels:join
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

In a secret named cypress_context_conf of the project P, store the following 
information:

```yaml
team_id: the team_id T
signin_url: the url of the Slack workspace T
cypress_slack_token: the slack token of the cypress Slack app
cypress_user_id: the user_id of the cypress Slack app
app_user_id: the user_id of the Fictionary Slack app
users:
  - id: the user_id of A0
    email: email of A0
    password: password of A0
  - id: the user_id of A1
    email: email of A1
    password: password of A1
  - id: the user_id of A2
    email: email of A2
    password: password of A2
  - id: the user_id of A3
    email: email of A3
    password: password of A3
```

At the root of Firestore, create a collection named constants containing 
a single document named constants. Include the following information in this
document (it is used by all the games, not only by those of team T):

```yaml
home_url: the url of the website
slack_signing_secret: the slack signing secret of the Fictionary app
```

In the document /teams/T store the following information (these parameters
are only used by the games of T):

```yaml
max_guessers_per_game: 20
max_life_span: 3600
max_running_games: 5
max_running_games_per_organizer: 10
refresh_interval: 4
self_trigger_threshold: 60
slack_token: the slack token of the Fictionary app
tagging: false
time_to_guess: 600
time_to_vote: 300
trigger_cooldown: 30
```

You can then run the following command:

```shell
python context.py P setup_channels
```

It will create in Firestore a channels collection in the document T with 
specific parameters for each channel that will be used during the tests.

You have to create a bucket tests-P to store the test results.

Finally, to launch all the tests, you can run from the tests directory:

```shell
python run.py P
```

Instead of using the Pub/Sub and the Cloud Functions from P, you can emulate 
them locally to test quickly changes in the code. 

You can emulate Pub/Sub by running this command from the game directory:

```shell
python local_deploy.py P pubsub
```

You can emulate the Cloud Functions by running this command from the game 
directory:

```shell
python local_deploy.py P functions
```