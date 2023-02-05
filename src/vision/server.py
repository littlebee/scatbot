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
import logging


from flask import Flask, Response, send_from_directory, abort
from flask_cors import CORS

import cv2

from commons import constants
from commons import web_utils
from commons.base_camera import BaseCamera
from vision.camera_opencv import OpenCvCamera
from vision.recognition_provider import RecognitionProvider


app = Flask(__name__)
CORS(app, supports_credentials=True)

camera = OpenCvCamera()

if not constants.DISABLE_RECOGNITION_PROVIDER:
    recognition = RecognitionProvider(camera)


def gen_rgb_video(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()

        jpeg = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_rgb_video(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/stats')
def send_stats():
    (cpu_temp, *rest) = [
        int(i) / 1000 for i in
        os.popen(
            'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
    ]
    return web_utils.json_response(app, {
        "capture": BaseCamera.stats(),
        "recognition": "disabled" if constants.DISABLE_RECOGNITION_PROVIDER else RecognitionProvider.stats(),
    })


@app.route('/pauseRecognition')
def pause_recognition():
    if constants.DISABLE_RECOGNITION_PROVIDER:
        return abort(404, "recognition provider disabled")

    recognition.pause()
    return web_utils.respond_ok(app)


@app.route('/resumeRecognition')
def resume_recognition():
    if constants.DISABLE_RECOGNITION_PROVIDER:
        return abort(404, "recognition provider disabled")

    recognition.resume()
    return web_utils.respond_ok(app)


@app.route('/ping')
def ping():
    return web_utils.respond_ok(app, 'pong')


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
