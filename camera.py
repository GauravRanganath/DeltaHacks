import cv2


class VideoCamera(object):
    def __init__(self):
        # get video from webcam
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
