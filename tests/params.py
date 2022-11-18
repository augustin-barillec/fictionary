import copy
team_params = {
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
channel_default_params = copy.deepcopy(team_params)
channel_default_params['max_guessers_per_game'] = 3
channel_default_params['max_running_games'] = 100
channel_default_params['max_running_games_per_organizer'] = 100
channel_default_params['refresh_interval'] = 4
channel_default_params['tagging'] = True
channel_default_params['time_to_guess'] = 180
channel_default_params['time_to_vote'] = 180
