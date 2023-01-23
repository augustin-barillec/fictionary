import copy
import reusable
channel_default_params = copy.deepcopy(reusable.game_params.game_params)
channel_default_params['max_guessers_per_game'] = 3
channel_default_params['max_running_games'] = 100
channel_default_params['max_running_games_per_organizer'] = 100
channel_default_params['refresh_interval'] = 4
channel_default_params['tagging'] = True
channel_default_params['time_to_guess'] = 180
channel_default_params['time_to_vote'] = 180

channel_names = [
    'ending_bravo',
    'ending_hey',
    'ending_no_guesses',
    'ending_no_votes',
    'ending_thanks',
    'ending_well',
    'ending_winner',
    'ending_winners',
    'ending_zero',
    'exception_game_dead_open_view',
    'exception_game_dead_update_view',
    'exception_game_dead_view_response',
    'exception_guess_click_already_guessed',
    'exception_guess_click_organizer',
    'exception_guess_submission_max_these_guessers',
    'exception_guess_submission_no_time_left',
    'exception_pick_submission_not_between',
    'exception_pick_submission_not_integer',
    'exception_setup_submission_max_running',
    'exception_setup_submission_max_this_running',
    'exception_slash_command_invalid_parameter',
    'exception_slash_command_max_running',
    'exception_slash_command_max_this_running',
    'exception_slash_command_not_invited',
    'exception_vote_click_already_voted',
    'exception_vote_click_not_a_potential_voter',
    'exception_vote_submission_no_time_left',
    'setup_english',
    'setup_freestyle',
    'setup_french',
    'transition_guess_full_time',
    'transition_guess_shorten_time',
    'transition_vote_full_time',
    'transition_vote_shorten_time',
    'help',
    'special_characters']
channel_to_params = dict()
channel_to_user_indexes = dict()
channel_to_app_kicked = dict()
for n in channel_names:
    channel_to_params[n] = copy.deepcopy(channel_default_params)
    channel_to_user_indexes[n] = [0, 1, 2, 3]
    channel_to_app_kicked[n] = False

channel_to_params['ending_bravo']['max_guessers_per_game'] = 2
channel_to_params['ending_bravo']['time_to_vote'] = 20

channel_to_params['ending_hey']['max_guessers_per_game'] = 2
channel_to_params['ending_hey']['time_to_vote'] = 20

channel_to_params['ending_no_guesses']['time_to_guess'] = 0

channel_to_params['ending_no_votes']['max_guessers_per_game'] = 2
channel_to_params['ending_no_votes']['time_to_vote'] = 0

channel_to_params['ending_thanks']['time_to_guess'] = 20

channel_to_params['ending_well']['max_guessers_per_game'] = 2

channel_to_params['ending_winner']['max_guessers_per_game'] = 2

channel_to_params['ending_zero']['time_to_vote'] = 40

channel_to_params['exception_game_dead_open_view']['max_life_span'] = 10

channel_to_params['exception_game_dead_update_view']['max_life_span'] = 0

channel_to_params['exception_guess_submission_max_these_guessers'][
    'max_guessers_per_game'] = 2

channel_to_params['exception_guess_submission_no_time_left'][
    'time_to_guess'] = 20

channel_to_params['exception_setup_submission_max_running'][
    'max_running_games'] = 4

channel_to_params['exception_setup_submission_max_this_running'][
    'max_running_games_per_organizer'] = 2

channel_to_params['exception_slash_command_max_running'][
    'max_running_games'] = 3

channel_to_params['exception_slash_command_max_this_running'][
    'max_running_games_per_organizer'] = 2

channel_to_app_kicked['exception_slash_command_not_invited'] = True

channel_to_params['exception_vote_click_already_voted'][
    'max_guessers_per_game'] = 2

channel_to_params['exception_vote_click_not_a_potential_voter'][
    'max_guessers_per_game'] = 2

channel_to_params['exception_vote_submission_no_time_left'][
    'max_guessers_per_game'] = 2

channel_to_params['exception_vote_submission_no_time_left'][
    'time_to_vote'] = 20

channel_to_params['transition_guess_full_time']['time_to_guess'] = 40

channel_to_params['transition_guess_shorten_time'][
    'max_guessers_per_game'] = 2

channel_to_params['transition_vote_full_time']['max_guessers_per_game'] = 2
channel_to_params['transition_vote_full_time']['time_to_vote'] = 20

channel_to_params['transition_vote_shorten_time']['max_guessers_per_game'] = 2

channel_to_params['help']['max_running_games_per_organizer'] = 1
