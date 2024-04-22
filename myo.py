import multiprocessing

from pyomyo import Myo, emg_mode

_queue = multiprocessing.Queue()
def _worker(q):
    myo = Myo(mode=emg_mode.PREPROCESSED)
    myo.connect()

    def add_to_queue(emg, movement):
        q.put(emg)
    myo.add_emg_handler(add_to_queue)

    def print_battery(bat):
        print('Battery level:', bat)
    myo.add_battery_handler(print_battery)

    # vibrate to know we connected okay
    myo.vibrate(0.2)

    while True:
        myo.run()

def setup_myo() -> multiprocessing.Queue:
    process = multiprocessing.Process(target=_worker, args=(_queue,))
    process.start()
    return _queue
