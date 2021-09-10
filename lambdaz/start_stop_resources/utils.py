from datetime import datetime, time


def is_now_between(begin_time: time, end_time: time) -> bool:
    """
        Function to check if the current time is between a given time interval.
    """
    now = datetime.now().time()

    if begin_time < end_time:
        return begin_time <= now <= end_time
    else:  # crosses midnight
        return now >= begin_time or now <= end_time


def is_substring_in_string(substring: str, fullstring: str) -> bool:
    """
        Function to verify if a substring is part of a bigger string.
    """
    return substring in fullstring
