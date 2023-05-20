import datetime
import app.utils as ut


def compute_deadline(start_datetime, time_left):
    return start_datetime + datetime.timedelta(seconds=time_left)


def datetime1_minus_datetime2(d1, d2):
    return int((d1 - d2).total_seconds())


def seconds_to_minutes_seconds(seconds):
    return seconds // 60, seconds % 60


def build_time_display_for_timer(language, seconds):
    if seconds < 0:
        return ut.text.time_display[language].format(minutes=0, seconds=0)
    minutes, seconds = seconds_to_minutes_seconds(seconds)
    seconds_approx = seconds - seconds % 5
    return ut.text.time_display[language].format(
        minutes=minutes, seconds=seconds_approx)
