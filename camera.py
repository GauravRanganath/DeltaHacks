import cv2
from model import ASL_model
from PIL import Image, ImageDraw
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.asl_model = ASL_model()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)

        frame = cv2.resize(
            frame, (640, 480), interpolation=cv2.INTER_AREA)

        letter_to_get = 'B'
        ret, jpeg = cv2.imencode('.jpg', frame)

        result = self.asl_model.predict(frame, letter_to_get)
        print(result)

        return jpeg.tobytes()
