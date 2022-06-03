def build_game_id(
        slash_datetime_compact,
        team_id,
        channel_id,
        organizer_id,
        trigger_id):

    return f'{slash_datetime_compact}&{team_id}&{channel_id}' \
           f'&{organizer_id}&{trigger_id}'
