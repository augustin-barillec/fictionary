import reusable
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from app import utils


class Game:

    def __init__(
            self,
            game_id,
            surface_prefix,
            project_id,
            publisher,
            db):

        self.id = game_id
        self.surface_prefix = surface_prefix
        self.project_id = project_id
        self.publisher = publisher
        self.db = db

        self.team_id = utils.ids.game_id_to_team_id(self.id)
        self.channel_id = utils.ids.game_id_to_channel_id(self.id)
        self.organizer_id = utils.ids.game_id_to_organizer_id(self.id)

        self.surface_id_builder = utils.ids.SurfaceIdBuilder(
            self.surface_prefix, self.id)

        self.stage_triggerer = utils.pubsub.StageTriggerer(
            self.publisher, self.project_id, self.id)

        self.firestore_reader = utils.firestore.FirestoreReader(
            self.db, self.id)
        self.ref = self.firestore_reader.get_game_ref()
        self.team_dict = self.firestore_reader.get_team_dict()

        slack_token = self.team_dict['slack_token']
        self.slack_client = WebClient(slack_token)

        slack_signing_secret = self.team_dict['slack_signing_secret']
        self.slack_verifier = SignatureVerifier(slack_signing_secret)

        channel_dicts = self.firestore_reader.get_channel_dicts()
        if self.channel_id in channel_dicts:
            params = self.firestore_reader.get_channel_dict()
        else:
            params = self.team_dict

        self.max_guessers_per_game = params['max_guessers_per_game']
        self.max_life_span = params['max_life_span']
        self.max_running_games_per_organizer = \
            params['max_running_games_per_organizer']
        self.max_running_games = params['max_running_games']
        self.refresh_interval = params['refresh_interval']
        self.self_trigger_threshold = params['self_trigger_threshold']
        self.tagging = params['tagging']
        self.time_to_guess = params['time_to_guess']
        self.time_to_vote = params['time_to_vote']
        self.trigger_cooldown = params['trigger_cooldown']

        assert self.trigger_cooldown < self.self_trigger_threshold

        self.exists = True
        self.dict = self.firestore_reader.get_game_dict()
        if self.dict is None:
            self.exists = False
            return

        self.frozen_guessers = self.dict.get('frozen_guessers')
        self.frozen_voters = self.dict.get('frozen_voters')
        self.guess_deadline = self.dict.get('guess_deadline')
        self.guess_stage_last_trigger = self.dict.get(
            'guess_stage_last_trigger')
        self.guess_stage_over = self.dict.get('guess_stage_over')
        self.guess_start = self.dict.get('guess_start')
        self.guessers = self.dict.get('guessers')
        self.indexed_signed_proposals = self.dict.get(
            'indexed_signed_proposals')
        self.lower_ts = self.dict.get('lower_ts')
        self.max_guessers = self.dict.get('max_guessers')
        self.max_score = self.dict.get('max_score')
        self.parameter = self.dict.get('parameter')
        self.potential_voters = self.dict.get('potential_voters')
        self.pre_guess_stage_already_triggered = self.dict.get(
            'pre_guess_stage_already_triggered')
        self.pre_result_stage_already_triggered = self.dict.get(
            'pre_result_stage_already_triggered')
        self.pre_vote_stage_already_triggered = self.dict.get(
            'pre_vote_stage_already_triggered')
        self.question = self.dict.get('question')
        self.result_stage_over = self.dict.get('result_stage_over')
        self.results = self.dict.get('results')
        self.setup_submission = self.dict.get('setup_submission')
        self.tag = self.dict.get('tag')
        self.truth = self.dict.get('truth')
        self.truth_index = self.dict.get('truth_index')
        self.upper_ts = self.dict.get('upper_ts')
        self.version = self.dict.get('version')
        self.vote_deadline = self.dict.get('vote_deadline')
        self.vote_stage_last_trigger = self.dict.get('vote_stage_last_trigger')
        self.vote_stage_over = self.dict.get('vote_stage_over')
        self.vote_start = self.dict.get('vote_start')
        self.voters = self.dict.get('voters')
        self.winners = self.dict.get('winners')

        self.now = reusable.time.get_now()

        if self.guess_deadline is not None:
            self.time_left_to_guess = utils.time.datetime1_minus_datetime2(
                self.guess_deadline, self.now)

        if self.vote_deadline is not None:
            self.time_left_to_vote = utils.time.datetime1_minus_datetime2(
                self.vote_deadline, self.now)

        if self.max_guessers is not None and self.guessers is not None:
            self.nb_remaining_potential_guessers = (
                    self.max_guessers - len(self.guessers))

        if self.potential_voters is not None and self.voters is not None:
            self.remaining_potential_voters = utils.users.\
                compute_remaining_potential_voters(
                    self.potential_voters, self.voters)
