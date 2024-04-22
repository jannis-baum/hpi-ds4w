import multiprocessing

from pyomyo import Myo, emg_mode

_queue = multiprocessing.Queue()
_exit_event = multiprocessing.Event()

def _worker(queue, exit_event):
    myo = Myo(mode=emg_mode.PREPROCESSED)
    myo.connect()

    def add_to_queue(emg, movement):
        queue.put(emg)
    myo.add_emg_handler(add_to_queue)

    def print_battery(bat):
        print('Battery level:', bat)
    myo.add_battery_handler(print_battery)

    # vibrate to know we connected okay
    myo.vibrate(0.2)

    while not exit_event.is_set():
        myo.run()

def stop_myo():
    _exit_event.set()

def setup_myo():
    process = multiprocessing.Process(target=_worker, args=(_queue, _exit_event))
    process.start()
    return _queue
