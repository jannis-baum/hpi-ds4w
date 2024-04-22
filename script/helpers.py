import time

def _current_time():
    return round(time.time() * 1000)

_initial_time = _current_time()

# milliseconds since startup
def millis():
    return _current_time() - _initial_time
