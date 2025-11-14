import time
from flask import session

GAME_DURATION=90

def start_timer():
    session["start_time"]=time.time()

def get_remaining_time():
    start=session.get("start_time")
    if start is None:
        return GAME_DURATION

    elapsed=time.time()-start
    remaining = GAME_DURATION - int(elapsed)
    return max(0, remaining)

def is_time_over():
    return get_remaining_time() <= 0