import copy
import reusable
default_params = copy.deepcopy(reusable.game_params.game_params)
default_params['max_guessers_per_game'] = 3
default_params['max_running_games'] = 100
default_params['max_running_games_per_organizer'] = 100
default_params['refresh_interval'] = 4
default_params['tagging'] = True
default_params['time_to_guess'] = 180
default_params['time_to_vote'] = 180

suffixes = [
    'ending_draw',
    'ending_no_guesses',
    'ending_no_votes',
    'ending_one_guesser',
    'ending_one_voter_loser',
    'ending_one_voter_winner',
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
    'setup_automatic_pick',
    'setup_automatic_shuffle',
    'setup_freestyle',
    'transition_guess_full_time',
    'transition_guess_shorten_time',
    'transition_vote_full_time',
    'transition_vote_shorten_time',
    'help',
    'special_characters']
suffix_to_params = dict()
suffix_to_user_indexes = dict()
suffix_to_app_kicked = dict()
for s in suffixes:
    suffix_to_params[s] = copy.deepcopy(default_params)
    suffix_to_user_indexes[s] = [0, 1, 2, 3]
    suffix_to_app_kicked[s] = False

suffix_to_params['ending_draw']['max_guessers_per_game'] = 2

suffix_to_params['ending_no_guesses']['time_to_guess'] = 0

suffix_to_params['ending_one_guesser']['time_to_guess'] = 20

suffix_to_params['ending_no_votes']['max_guessers_per_game'] = 2
suffix_to_params['ending_no_votes']['time_to_vote'] = 0

suffix_to_params['ending_one_voter_winner']['max_guessers_per_game'] = 2
suffix_to_params['ending_one_voter_winner']['time_to_vote'] = 20

suffix_to_params['ending_one_voter_loser']['max_guessers_per_game'] = 2
suffix_to_params['ending_one_voter_loser']['time_to_vote'] = 20

suffix_to_params['ending_winner']['max_guessers_per_game'] = 2

suffix_to_params['ending_zero']['time_to_vote'] = 40

suffix_to_params['exception_game_dead_open_view']['max_life_span'] = 10

suffix_to_params['exception_game_dead_update_view']['max_life_span'] = 0

suffix_to_params['exception_guess_submission_max_these_guessers'][
    'max_guessers_per_game'] = 2

suffix_to_params['exception_guess_submission_no_time_left'][
    'time_to_guess'] = 20

suffix_to_params['exception_setup_submission_max_running'][
    'max_running_games'] = 4

suffix_to_params['exception_setup_submission_max_this_running'][
    'max_running_games_per_organizer'] = 2

suffix_to_params['exception_slash_command_max_running'][
    'max_running_games'] = 3

suffix_to_params['exception_slash_command_max_this_running'][
    'max_running_games_per_organizer'] = 2

suffix_to_app_kicked['exception_slash_command_not_invited'] = True

suffix_to_params['exception_vote_click_already_voted'][
    'max_guessers_per_game'] = 2

suffix_to_params['exception_vote_click_not_a_potential_voter'][
    'max_guessers_per_game'] = 2

suffix_to_params['exception_vote_submission_no_time_left'][
    'max_guessers_per_game'] = 2

suffix_to_params['exception_vote_submission_no_time_left'][
    'time_to_vote'] = 20

suffix_to_params['transition_guess_full_time']['time_to_guess'] = 40

suffix_to_params['transition_guess_shorten_time'][
    'max_guessers_per_game'] = 2

suffix_to_params['transition_vote_full_time']['max_guessers_per_game'] = 2
suffix_to_params['transition_vote_full_time']['time_to_vote'] = 20

suffix_to_params['transition_vote_shorten_time']['max_guessers_per_game'] = 2

suffix_to_params['help']['max_running_games_per_organizer'] = 1

names = []
name_to_params = dict()
name_to_user_indexes = dict()
name_to_app_kicked = dict()
for language in ['English', 'French']:
    for s in suffixes:
        name = f'{language.lower()}_{s}'
        names.append(name)
        name_to_params[name] = copy.deepcopy(suffix_to_params[s])
        name_to_params[name]['language'] = language
        name_to_user_indexes[name] = copy.deepcopy(suffix_to_user_indexes[s])
        name_to_app_kicked[name] = copy.deepcopy(suffix_to_app_kicked[s])
