from argparse import ArgumentParser

import cv2
import pandas as pd

from helpers import millis
from myo import setup_myo, stop_myo

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    queue = setup_myo()

    df = pd.DataFrame(columns=['millis', *[f'EMG{i}' for i in range(8)]])

    size = (480, 270)
    cap = cv2.VideoCapture(0)
    writer = cv2.VideoWriter(f'{args.output}.mp4', cv2.VideoWriter_fourcc(*'AVC1'), 20, size)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
             print("Can't receive frame (stream end?). Exiting ...")
             break
        frame = cv2.resize(cv2.flip(frame, 1), size)
        
        writer.write(frame)
        cv2.imshow('frame', frame)

        while not(queue.empty()):
            emg = list(queue.get())
            time = millis()
            df.loc[len(df)] = [time, *emg]
            print(('{:7}: ' + ' | '.join(['{:4}'] * 8)).format(time, *emg))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop_myo()
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    df.to_csv(f'{args.output}.csv', index=False)
    quit()
