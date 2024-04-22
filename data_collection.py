from argparse import ArgumentParser
import os

from cv2.typing import MatLike
import pandas as pd

from helpers import millis
from myo import setup_myo, stop_myo
from video import VideoRecorder

if __name__ == '__main__':
    # argument parsing & outputs
    parser = ArgumentParser()
    parser.add_argument('output', type=str)
    args = parser.parse_args()
    os.mkdir(args.output)
    def path(component: str):
        return os.path.join(args.output, component)

    # myo setup
    queue = setup_myo()
    df = pd.DataFrame(columns=['millis', *[f'EMG{i}' for i in range(8)]])

    def frame_handler(frame: MatLike) -> MatLike:
        while not(queue.empty()):
            emg = list(queue.get())
            time = millis()
            df.loc[len(df)] = [time, *emg]
            print(('{:7}: ' + ' | '.join(['{:4}'] * 8)).format(time, *emg))
        return frame

    rec = VideoRecorder(frame_handler, path('video.mp4'))
    rec.run()

    # myo teardown
    stop_myo()
    df.to_csv(path('data.csv'), index=False)
