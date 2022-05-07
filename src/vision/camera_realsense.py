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

import pyrealsense2 as rs
import numpy as np

from commons import constants
from vision.base_camera import BaseCamera

logger = logging.getLogger(__name__)


class RealsenseCamera(BaseCamera):
    video_source = 0
    img_is_none_messaged = False

    def __init__(self):
        RealsenseCamera.set_video_source(constants.CAMERA_CHANNEL_RGB)
        super(RealsenseCamera, self).__init__()

    @staticmethod
    def set_video_source(source):
        RealsenseCamera.video_source = source

    @staticmethod
    def frames():
        logger.info('initializing VideoCapture')

        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = rs.pipeline()

        # Configure streams
        config = rs.config()
        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        pipeline.start(config)

        while True:

            # This call waits until a new coherent set of frames is available on a device
            # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            # depth_frame = frames.get_depth_frame()

            color_image = np.asanyarray(color_frame.get_data())
            # depth_image = np.asanyarray(depth_frame.get_data())

            if color_image is None:
                if not RealsenseCamera.img_is_none_messaged:
                    logger.error(
                        "The camera has not read data, please check whether the camera can be used normally.")
                    logger.error(
                        "Use the command: 'raspistill -t 1000 -o image.jpg' to check whether the camera can be used correctly.")
                    RealsenseCamera.img_is_none_messaged = True
                continue

            yield color_image
