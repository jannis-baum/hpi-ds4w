from typing import Callable

import cv2
from cv2.typing import MatLike


class VideoRecorder:
    def __init__(
        self,
        loop_callback: Callable[[MatLike], MatLike],
        save_path: str | None = None,
        resize: tuple[int, int] = (480, 270),
        out_size: tuple[int, int] = (480, 270)
    ):
        self.resize = resize
        self.loop_callback = loop_callback
        self.cap = cv2.VideoCapture(0)
        if save_path:
            self.writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'AVC1'), 20, out_size)
        else:
            self.writer = None

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                 print("Can't receive frame (stream end?). Exiting ...")
                 break

            frame = cv2.resize(cv2.flip(frame, 1), self.resize)
            frame = self.loop_callback(frame)

            if self.writer:
                self.writer.write(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
