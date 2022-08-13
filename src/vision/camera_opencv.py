"""
 This was originally pilfered from
 https://github.com/adeept/Adeept_RaspTank/blob/a6c45e8cc7df620ad8977845eda2b839647d5a83/server/camera_opencv.py

 Which looks like it was in turn pilfered from
 https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited

"Great artists steal". Thank you, @adeept and @miguelgrinberg!
"""

import os
import cv2
import logging

from commons import constants
from commons.base_camera import BaseCamera

logger = logging.getLogger(__name__)


class OpenCvCamera(BaseCamera):
    video_source = 0
    img_is_none_messaged = False

    def __init__(self):
        OpenCvCamera.set_video_source(constants.CAMERA_CHANNEL_PICAM)
        super(OpenCvCamera, self).__init__()

    @staticmethod
    def set_video_source(source):
        print(f"setting video source to {source}")
        OpenCvCamera.video_source = source

    @staticmethod
    def frames():
        print('initializing VideoCapture')

        camera = cv2.VideoCapture(
            OpenCvCamera.video_source)  # , apiPreference=cv2.CAP_V4L2)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        while True:
            _, img = camera.read()
            if img is None:
                if not OpenCvCamera.img_is_none_messaged:
                    logger.error(
                        "The camera has not read data, please check whether the camera can be used normally.")
                    logger.error(
                        "Use the command: 'raspistill -t 1000 -o image.jpg' to check whether the camera can be used correctly.")
                    OpenCvCamera.img_is_none_messaged = True
                continue

            yield img
