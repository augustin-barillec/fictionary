from copy import deepcopy

default_params = {
    'max_guessers_per_game': 100,
    'max_life_span': 3600,
    'max_running_games': 100,
    'max_running_games_per_organizer': 100,
    'refresh_interval': 9,
    'self_trigger_threshold': 60,
    'tagging': True,
    'time_to_guess': 300,
    'time_to_vote': 600,
    'trigger_cooldown': 30
}

channel_names = [
    'ending_no_guesses',
    'ending_thanks',
    'ending_no_votes',
    'ending_bravo',
    'ending_hey',
    'ending_zero',
    'ending_well',
    'ending_winner',
    'ending_winners',
    'exception_slash_command_max_this_running',
    'exception_slash_command_not_invited',
    'exception_slash_command_max_running',
    'exception_setup_submission_max_this_running',
    'exception_setup_submission_max_running',
    'exception_guess_submission_no_time_left',
    'exception_guess_submission_max_these_guessers',
    'exception_vote_submission_no_time_left',
    'exception_guess_click_organizer',
    'exception_guess_click_already_guessed',
    'exception_guess_click_not_a_member',
    'exception_guess_click_max_these_guessers',
    'exception_vote_click_not_a_potential_voter',
    'exception_vote_click_already_voted',
    'setup_english',
    'setup_freestyle',
    'setup_french',
    'transition_guess_full',
    'transition_guess_shorten',
    'transition_vote_full',
    'transition_vote_shorten',
    'special_characters'
]

channel_to_params = dict()
channel_to_user_indexes = dict()
channel_to_app_kicked = dict()
for n in channel_names:
    channel_to_params[n] = deepcopy(default_params)
    channel_to_user_indexes[n] = [0, 1, 2, 3]
    channel_to_app_kicked[n] = False

channel_to_params['ending_no_guesses']['time_to_guess'] = 5

channel_to_params['ending_thanks']['time_to_guess'] = 35

channel_to_params['ending_no_votes']['time_to_vote'] = 1
channel_to_user_indexes['ending_no_votes'] = [0, 1, 2]

channel_to_params['ending_bravo']['time_to_vote'] = 40
channel_to_user_indexes['ending_bravo'] = [0, 1, 2]

channel_to_params['ending_hey']['time_to_vote'] = 30
channel_to_user_indexes['ending_hey'] = [0, 1, 2]

channel_to_params['ending_zero']['time_to_vote'] = 80

channel_to_user_indexes['ending_well'] = [0, 1, 2]

channel_to_user_indexes['ending_winner'] = [0, 1, 2]

channel_to_params['exception_slash_command_max_this_running'][
    'max_running_games_per_organizer'] = 2

channel_to_app_kicked['exception_slash_command_not_invited'] = True

channel_to_params['exception_slash_command_max_running'][
    'max_running_games'] = 3
channel_to_params['exception_slash_command_max_running'][
    'self_trigger_threshold'] = 0

channel_to_params['exception_setup_submission_max_this_running'][
    'max_running_games_per_organizer'] = 2

channel_to_params['exception_setup_submission_max_running'][
    'max_running_games'] = 4
channel_to_params['exception_setup_submission_max_running'][
    'self_trigger_threshold'] = 0

channel_to_params['exception_guess_submission_no_time_left'][
    'time_to_guess'] = 35

channel_to_params['exception_guess_submission_max_these_guessers'][
    'max_guessers_per_game'] = 5

channel_to_params['exception_vote_submission_no_time_left'][
    'time_to_vote'] = 35
channel_to_user_indexes['exception_vote_submission_no_time_left'] = [0, 1, 2]

channel_to_user_indexes['exception_guess_click_not_a_member'] = [0, 1]

channel_to_params['exception_guess_click_max_these_guessers'][
    'max_guessers_per_game'] = 2

channel_to_params['exception_vote_click_not_a_potential_voter'][
    'time_to_guess'] = 70

channel_to_user_indexes['exception_vote_click_already_voted'] = [0, 1, 2]

channel_to_params['transition_guess_full']['time_to_guess'] = 80

channel_to_user_indexes['transition_guess_shorten'] = [0, 1, 2]

channel_to_user_indexes['transition_vote_full'] = [0, 1, 2]
channel_to_params['transition_vote_full']['time_to_vote'] = 35

channel_to_user_indexes['transition_vote_shorten'] = [0, 1, 2]
