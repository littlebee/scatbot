#!/usr/bin/env python3
"""
 This was originally pilfered from
 https://github.com/adeept/Adeept_RaspTank/blob/a6c45e8cc7df620ad8977845eda2b839647d5a83/server/app.py

 Which looks like it was in turn pilfered from
 https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited

"Great artists steal". Thank you, @adeept and @miguelgrinberg!
"""

import os
import threading
import json
import psutil
import logging
from enum import Enum


from flask import Flask, Response, send_from_directory, abort
from flask_cors import CORS

import cv2

from vision.camera_opencv import OpenCvCamera
from vision.camera_realsense import RealsenseCamera
from vision.base_camera import BaseCamera
from vision.recognition import Recognition
from vision.depth_provider import DepthProvider

from commons import constants


app = Flask(__name__)
CORS(app, supports_credentials=True)


class CAMERAS(Enum):
    opencv = 0
    realsense = 1
    # future maybe
    # picamera = 2


which_camera = None
if os.getenv('USE_OPENCV') != None:
    print("Will use opencv camera")
    which_camera = CAMERAS.opecv
else:
    print("Will use realsense camera")
    which_camera = CAMERAS.realsense

camera = None
if which_camera == CAMERAS.opencv:
    camera = OpenCvCamera()
else:
    camera = RealsenseCamera()

recognition = Recognition(camera)
depth = DepthProvider(camera)


def gen_rgb_video(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        # can't augment the frame directly from the camera as that will
        # alter it for all and you will see the face detection start to
        # stutter and blank out
        frame = frame.copy()

        # add names and bounding boxes
        frame = recognition.augment_frame(frame)
        jpeg = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')


def gen_depth_video(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_depth_image()
        jpeg = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')


def json_response(data):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


def respond_ok(data=None):
    return json_response({
        "status": "ok",
        "data": data
    })


def respond_not_ok(status, data):
    return json_response({
        "status": status,
        "data": data
    })


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_rgb_video(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/depth_feed')
def depth_feed():
    """Colorized depth map streaming route. Put this in the src attribute of an img tag."""
    if which_camera == CAMERAS.opencv:
        abort(404, "depth image not support by camera")
    return Response(gen_depth_video(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/stats')
def send_stats():
    (cpu_temp, *rest) = [
        int(i) / 1000 for i in
        os.popen(
            'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
    ]
    return json_response({
        "capture": BaseCamera.stats(),
        "recognition": Recognition.stats(),
        "depthProvider": DepthProvider.stats(),
    })


@app.route('/pauseRecognition')
def pause_recognition():
    recognition.pause()
    return respond_ok()


@app.route('/resumeRecognition')
def resume_recognition():
    recognition.resume()
    return respond_ok()


@app.route('/ping')
def ping():
    return respond_ok('pong')


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(dir_path, filename)


@app.route('/')
def index():
    return send_from_directory(dir_path, 'index.html')


class webapp:
    def __init__(self):
        self.camera = camera

    def thread(self):
        app.run(host='0.0.0.0', port=constants.VISION_PORT, threaded=True)

    def start_thread(self):
        # Define a thread for FPV and OpenCV
        thread = threading.Thread(target=self.thread)
        # 'True' means it is a front thread,it would close when the mainloop() closes
        thread.setDaemon(False)
        thread.start()  # Thread starts


def start_app():
    # setup_logging('ai.log')
    logger = logging.getLogger(__name__)
    logger.info('vision service started')

    flask_app = webapp()
    flask_app.start_thread()
