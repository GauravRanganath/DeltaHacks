import cv2
from model import ASL_model
from PIL import Image, ImageDraw


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.asl_model = ASL_model()
        self.result = False
        self.letter_to_get = 'A'

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)

        frame = cv2.resize(
            frame, (640, 480), interpolation=cv2.INTER_AREA)

        ret, jpeg = cv2.imencode('.jpg', frame)
        result = self.asl_model.predict(frame, self.letter_to_get)

        if result is True:
            print("\nYou correctly signed: ", self.letter_to_get + '\n')
            self.letter_to_get = chr(ord(self.letter_to_get) + 1)

        return jpeg.tobytes()
