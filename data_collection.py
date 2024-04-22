from argparse import ArgumentParser

import pandas as pd

from helpers import millis
from myo import setup_myo

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    queue = setup_myo()

    df = pd.DataFrame(columns=['millis', *[f'EMG{i}' for i in range(8)]])

    try:
        while True:
            while not(queue.empty()):
                emg = list(queue.get())
                time = millis()
                df.loc[len(df)] = [time, *emg]
                print(('{:7}: ' + ' | '.join(['{:4}'] * 8)).format(time, *emg))
    except KeyboardInterrupt:
        print('Quitting')

    df.to_csv(f'{args.output}.csv', index=False)
