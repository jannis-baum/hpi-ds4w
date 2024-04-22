import multiprocessing

import pandas as pd
from pyomyo import Myo, emg_mode

from helpers import millis

q = multiprocessing.Queue()
def worker(q):
    m = Myo(mode=emg_mode.PREPROCESSED)
    m.connect()
    
    def add_to_queue(emg, movement):
        q.put(emg)
    m.add_emg_handler(add_to_queue)
    
    def print_battery(bat):
        print('Battery level:', bat)
    m.add_battery_handler(print_battery)

    # vibrate to know we connected okay
    m.vibrate(0.2)
    
    while True:
        m.run()

if __name__ == '__main__':
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()

    df = pd.DataFrame(columns=['millis', *[f'EMG{i}' for i in range(8)]])

    try:
        while True:
            while not(q.empty()):
                emg = list(q.get())
                time = millis()
                df.loc[len(df)] = [time, *emg]
                print(('{:7}: ' + ' | '.join(['{:4}'] * 8)).format(time, *emg))

    except KeyboardInterrupt:
        print('Quitting')

    df.to_csv('data.csv', index=False)
