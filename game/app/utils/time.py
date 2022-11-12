import datetime


def compute_deadline(start_datetime, time_left):
    return start_datetime + datetime.timedelta(seconds=time_left)


def datetime1_minus_datetime2(d1, d2):
    return int((d1 - d2).total_seconds())


def compute_time_left(now, deadline):
    return datetime1_minus_datetime2(deadline, now)


def seconds_to_minutes_seconds(seconds):
    return seconds // 60, seconds % 60


def build_time_display_for_timer(seconds):
    if seconds < 0:
        return '0min 0s'
    minutes, seconds = seconds_to_minutes_seconds(seconds)
    seconds_approx = seconds - seconds % 5
    return f'{minutes}min {seconds_approx}s'


def build_time_display_for_setup_view(seconds):
    minutes, seconds = seconds_to_minutes_seconds(seconds)
    res = f'{minutes}min'
    if seconds != 0:
        res += f' {seconds}s'
    return res
