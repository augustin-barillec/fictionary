port_infos = {
    5000: ('slash_command', 'http'),
    5001: ('message_actions', 'http'),
    5002: ('pre_guess_stage', 'event'),
    5003: ('guess_stage', 'event'),
    5004: ('pre_vote_stage', 'event'),
    5005: ('vote_stage', 'event'),
    5006: ('pre_result_stage', 'event'),
    5007: ('result_stage', 'event'),
    5008: ('freeze', 'event'),
}
ports = sorted(port_infos)
port_to_function_name = {port: port_infos[port][0] for port in ports}
port_to_signature_type = {port: port_infos[port][1] for port in ports}
