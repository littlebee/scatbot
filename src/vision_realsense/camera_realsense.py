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
import math

import cv2
import numpy

# on raspbery pi zero:
# import pyrealsense2.pyrealsense2 as rs
# on raspbery pi 4:
import pyrealsense2 as rs

import numpy as np

from commons import constants
from commons.base_camera import BaseCamera, CameraEvent

logger = logging.getLogger(__name__)

DECIMATE_PURE_PY = 0
DECIMATE_REALSENSE = 1
DECIMATE_NUMPY = 2

DECIMATE_METHOD = constants.env_int('DECIMATE_METHOD', DECIMATE_NUMPY)


class RealsenseCamera(BaseCamera):
    video_source = 0
    img_is_none_messaged = False

    last_depth_data = []
    last_depth_image = None
    depth_frame_event = CameraEvent()


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
        RealsenseCamera.depth_frame_event.wait()
        RealsenseCamera.depth_frame_event.clear()

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
        if not constants.DISABLE_REALSENSE_RECOGNITION:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        if not constants.DISABLE_DEPTH_PROVIDER:
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        # align_to = rs.stream.color
        # align = rs.align(align_to)

        # Start streaming
        pipeline.start(config)

        while True:
            try:
                # This call waits until a new coherent set of frames is available on a device
                # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
                frames = pipeline.wait_for_frames()

                ## This would align the depth_frame with the color frame, but...
                ## It's so freaking slow.  Capture FPS when from 29 fps down to
                ## 7 fps  and CPU utilization went from 26% to 36%
                # frames = align.process(frames)

                color_image = None
                if not constants.DISABLE_REALSENSE_RECOGNITION:
                    color_frame = frames.get_color_frame()
                    color_image = np.asanyarray(color_frame.get_data())

                if not constants.DISABLE_DEPTH_PROVIDER:
                    depth_frame = frames.get_depth_frame()
                    full_depth_data = np.asanyarray(depth_frame.get_data())
                    depth_image = cv2.applyColorMap(
                        cv2.convertScaleAbs(full_depth_data, alpha=0.03),
                        cv2.COLORMAP_JET)

                    depth_data = RealsenseCamera._decimate_depth_data(depth_frame, full_depth_data)

                    RealsenseCamera.last_depth_data = depth_data
                    RealsenseCamera.last_depth_image = depth_image
                    RealsenseCamera.depth_frame_event.set()

                if color_image is None and not constants.DISABLE_REALSENSE_RECOGNITION:
                    if not RealsenseCamera.img_is_none_messaged:
                        logger.error(
                            "The camera has not read data, please check whether the camera can be used normally.")
                        logger.error(
                            "Use the command: 'raspistill -t 1000 -o image.jpg' to check whether the camera can be used correctly.")
                        RealsenseCamera.img_is_none_messaged = True
                    continue


                yield color_image if not constants.DISABLE_REALSENSE_RECOGNITION else depth_image

            except:
                traceback.print_exc()
                print("Failed to fetch frame from realsense camera. Waiting 5 seconds and retrying...")
                time.sleep(5)


    @staticmethod
    def _decimate_depth_data(depth_frame, depth_data):
        if DECIMATE_METHOD == DECIMATE_PURE_PY:
            return RealsenseCamera._decimate_pure_py(depth_frame, depth_data)
        elif DECIMATE_METHOD == DECIMATE_REALSENSE:
            return RealsenseCamera._decimate_realsense(depth_frame, depth_data)
        elif DECIMATE_METHOD == DECIMATE_NUMPY:
            return RealsenseCamera._decimate_numpy(depth_frame, depth_data)

        return [[]]


    @staticmethod
    def _decimate_pure_py(depth_frame, depth_data):
        """
            This is, as it turns out, a really slow way to do
            it.  (like 0.2 FPS slow)
        """
        target_width = constants.DEPTH_MAP_SECTION_WIDTH
        target_height = constants.DEPTH_MAP_SECTION_HEIGHT

        dec_depth_data = [
            [0]*target_width for i in range(target_height)]

        y_div = len(depth_data) / target_height

        for iy, line in enumerate(depth_data):
            x_div = len(line) / target_width
            section_y = int(iy / y_div)
            for ix, value in enumerate(line):
                if value > 0:
                    section_x = int(ix / x_div)
                    sec_depth = dec_depth_data[section_y][section_x]
                    if sec_depth == 0 or value < sec_depth:
                        dec_depth_data[section_y][section_x] = int(value)

        return dec_depth_data


    @staticmethod
    def _decimate_realsense(depth_frame, depth_data):
        """
            This is the fastest, but data is not 5x5 and edges
            of the matrix (last two columns and last row)
            are all zero after
        """
        # Running it though the filter twice at the max divisor
        # of 8 produces a 12 x 8 array of ranges which is still more
        # than scatbot needs but is much faster than the earlier implementation
        # I did in python
        dec_depth_frame = rs.decimation_filter(8).process(depth_frame)
        dec_depth_frame = rs.decimation_filter(8).process(dec_depth_frame)

        return np.asanyarray(dec_depth_frame.get_data()).tolist()

    @staticmethod
    def _decimate_numpy(depth_frame, depth_data):
        """
            This is also pretty fast (25fps)
        """
        target_width = constants.DEPTH_MAP_SECTION_WIDTH
        target_height = constants.DEPTH_MAP_SECTION_HEIGHT
        [data_width, data_height] = depth_data.shape

        block_width = int(data_width / target_width)
        block_height = int(data_height / target_height)

        # print(f"block_width={block_width} block_height={block_height}")

        dec_depth_data = [
            [0]*target_width for i in range(target_height)]

        for x in range(target_width):
            data_x = x * block_width
            for y in range(target_height):
                data_y = y * block_width
                # print(f"({x}, {y}) = ({data_x}, {data_y})")
                section = depth_data[data_x:data_x + block_width, data_y:data_y + block_height]
                # print(f"({x}, {y}) : section={section}")
                section_nonzero = section[section != 0]
                # print(f"({x}, {y}) : section_nonzero={section_nonzero}")

                value = int(section_nonzero.min()) if len(section_nonzero) > 0 else 0
                # print(f"({x}, {y}) = {value}")
                dec_depth_data[x][y] = value

        return dec_depth_data
        # return sections.tolist()