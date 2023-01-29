"""
 This was originally pilfered from
 https://github.com/adeept/Adeept_RaspTank/blob/a6c45e8cc7df620ad8977845eda2b839647d5a83/server/camera_opencv.py

 Which looks like it was in turn pilfered from
 https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited

"Great artists steal". Thank you, @adeept and @miguelgrinberg!
"""

import os
import time
import logging
import traceback


import cv2

# on raspbery pi zero:
# import pyrealsense2.pyrealsense2 as rs
# on raspbery pi 4:
import pyrealsense2 as rs

import numpy as np

from commons import constants
from commons.base_camera import BaseCamera

logger = logging.getLogger(__name__)


class RealsenseCamera(BaseCamera):
    video_source = 0
    img_is_none_messaged = False

    last_depth_data = []
    last_depth_image = None

    def __init__(self):
        RealsenseCamera.set_video_source(constants.CAMERA_CHANNEL_RS)
        super(RealsenseCamera, self).__init__()

    def get_depth_image(self):
        """Return the last colorized depth image."""
        RealsenseCamera.last_depth_image_access = time.time()

        return RealsenseCamera.last_depth_image

    def get_depth_data(self):
        """Return the last depth map (not colorized)."""
        RealsenseCamera.last_depth_data_access = time.time()

        return RealsenseCamera.last_depth_data

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
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        align_to = rs.stream.color
        align = rs.align(align_to)

        # Start streaming
        pipeline.start(config)

        while True:
            try:
                # This call waits until a new coherent set of frames is available on a device
                # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
                frames = pipeline.wait_for_frames()

                # This would align the depth_frame with the color frame, but...
                # It's so freaking slow.  Capture FPS when from 29 fps down to
                # 7 fps  and CPU utilization went from 26% to 36%
                # frames = align.process(frames)

                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()

                color_image = np.asanyarray(color_frame.get_data())
                depth_data = np.asanyarray(depth_frame.get_data())
                depth_image = cv2.applyColorMap(cv2.convertScaleAbs(
                    depth_data, alpha=0.03), cv2.COLORMAP_JET)

                if color_image is None:
                    if not RealsenseCamera.img_is_none_messaged:
                        logger.error(
                            "The camera has not read data, please check whether the camera can be used normally.")
                        logger.error(
                            "Use the command: 'raspistill -t 1000 -o image.jpg' to check whether the camera can be used correctly.")
                        RealsenseCamera.img_is_none_messaged = True
                    continue

                RealsenseCamera.last_depth_data = depth_data
                RealsenseCamera.last_depth_image = depth_image

                yield color_image

            except:
                traceback.print_exc()
                print("Failed to fetch frame from realsense camera. Waiting 5 seconds and retrying...")
                time.sleep(5)
