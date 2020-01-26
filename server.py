from flask import Flask, render_template, Response, request
from camera import VideoCamera
import requests
from PIL import Image, ImageDraw
import cv2
import io
import time


app = Flask(__name__, static_folder="static")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/streaming')
def webcam():
    return render_template('streaming.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        frame_img = Image.open(io.BytesIO(frame))

        width, height = frame_img.size
        x_0 = int(width * 0.1)
        y_0 = int(height * 0.25)
        x_1 = int(x_0 + 200)
        y_1 = int(y_0 + 200)

        x, y = (x_0, y_0), (x_1, y_1)

        temp = ImageDraw.ImageDraw(frame_img)
        temp.rectangle(
            xy=[x, y], fill=None, outline="red", width=5)

        frame = img_to_byte_array(frame_img)

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/video_feed', methods=['POST'])
def api_video_feed():
    data = request.args.get('frame')
    return "Hello"


@app.route('/streaming-2')
def webcam2():
    return render_template('streaming-2.html')


@app.route('/streaming-3')
def webcam3():
    return render_template('streaming-3.html')


def img_to_byte_array(img):
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format=img.format)
    img_byte_array = img_byte_array.getvalue()
    return img_byte_array


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
