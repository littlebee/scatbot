#!/usr/bin/env python3
"""
    This is a vision server for scatbot that provides both rgb video and
    depth video from the Intel Realsense D435i camera.

    depth_provider.py publishes the depth_map as a smaller array of minimum
    distances to the `depth_map` key of central hub state.

    It also uses the recognition_provider from the base vision package to provide
    the `recognition` key to central hub state.

"""

import os
import threading
import logging
from enum import Enum


from flask import Flask, Response, send_from_directory, abort
from flask_cors import CORS

import cv2

from commons.base_camera import BaseCamera
from commons import web_utils
from commons import constants
from vision.recognition_provider import RecognitionProvider
from vision_realsense.camera_realsense import RealsenseCamera
from vision_realsense.depth_provider import DepthProvider


DISABLE_DEPTH_PROVIDER = os.getenv('DISABLE_DEPTH_PROVIDER') or False
DISABLE_RECOGNITION_PROVIDER = os.getenv('DISABLE_RECOGNITION_PROVIDER') or False

app = Flask(__name__)
CORS(app, supports_credentials=True)

camera = RealsenseCamera()

if not DISABLE_DEPTH_PROVIDER:
    depth = DepthProvider(camera)
else:
    print('Depth provider disabled');

if not DISABLE_RECOGNITION_PROVIDER:
    recognition = RecognitionProvider(camera)
else:
    print('Recognition provider disabled');


def gen_rgb_video(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()

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


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_rgb_video(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/depth_feed')
def depth_feed():
    if DISABLE_DEPTH_PROVIDER:
        abort(404, "depth camera disabled")
        return

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
    return web_utils.json_response(app, {
        "cpu_temp": cpu_temp,
        "capture": BaseCamera.stats(),
        "depthProvider": "disabled" if DISABLE_DEPTH_PROVIDER else DepthProvider.stats(),
        "recognition": "disabled" if DISABLE_RECOGNITION_PROVIDER else RecognitionProvider.stats()
    })


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
        app.run(host='0.0.0.0', port=constants.DEPTH_PORT, threaded=True)

    def start_thread(self):
        # Define a thread for FPV and OpenCV
        thread = threading.Thread(target=self.thread)
        # 'True' means it is a front thread,it would close when the mainloop() closes
        thread.setDaemon(False)
        thread.start()  # Thread starts


def start_app():
    # setup_logging('ai.log')
    logger = logging.getLogger(__name__)
    logger.info('vision_realsense service started')

    flask_app = webapp()
    flask_app.start_thread()
