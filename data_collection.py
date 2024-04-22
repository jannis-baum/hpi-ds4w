from argparse import ArgumentParser
import os
import cv2

from cv2.typing import MatLike
import numpy as np
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

    # plotting setup
    size = (480, 270)
    plot = np.zeros((*size[::-1], 3), np.uint8) # initial blank plot
    step = 3 # pixel offset the plot moves each frame
    prev_emgs: list | None = None # previous measurement to draw lines from
    emg_max = 1500 # emg values are unpacked from a 16 byte unsigned int so
                   # technically it could go to 2^16 but i haven't seen
                   # anything much over 1000

    def frame_handler(frame: MatLike) -> MatLike:
        global plot; global prev_emgs

        emgs = None
        while not(queue.empty()):
            emgs = list(queue.get())
            time = millis()
            df.loc[len(df)] = [time, *emgs]
            print(('{:7}: ' + ' | '.join(['{:4}'] * 8)).format(time, *emgs))

        # shift plot to the left
        plot = np.roll(plot, -step, axis=1)
        plot[:, -step:, :] = 0
        # draw new plots
        if emgs:
            for i, emg in enumerate(emgs):
                height = int(size[1] / len(emgs))
                # y of upper left pixel of plotting row we are in
                y_origin = height * i
                # separator lines
                cv2.line(plot, (0, y_origin), (size[0], y_origin), (255, 255, 255), 1)
                # actual line plot
                if prev_emgs:
                    # x coordinates of start & end of new line addition to plot
                    x1 = size[0]
                    x0 = x1 - step
                    # lower left pixel of plotting row
                    y_o_inverse = y_origin + height
                    # line scaled with emg_max & height
                    y0 = y_o_inverse - int(prev_emgs[i] / emg_max * height)
                    y1 = y_o_inverse - int(emg / emg_max * height)
                    cv2.line(plot, (x0, y0), (x1, y1), (255, 190, 115), 2)
            prev_emgs = emgs

        return np.concatenate((plot, frame), axis=0)

    rec = VideoRecorder(frame_handler, path('video.mp4'), resize=size, out_size=(size[0], size[1] * 2))
    rec.run()

    # myo teardown
    stop_myo()
    df.to_csv(path('data.csv'), index=False)
