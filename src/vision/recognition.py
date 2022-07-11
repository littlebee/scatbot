"""
This class detects faces in frames it gets from the camera object passed to
the constructor.

The get_objects method returns the bounding boxes for all faces last detected.

A thread is created that does the heavy lifting of detecting faces and updates
a class var that contains the last faces detected. This allows the thread providing
the video feed to stream at 30fps while face frames lag behind at 3fps (maybe upto 10?)
"""
import os
import time
import threading
import cv2
import numpy
import logging

from commons.fps_stats import FpsStats

logger = logging.getLogger(__name__)


class Recognition:
    thread = None  # background thread that reads frames from camera
    camera = None
    last_objects_seen = []
    last_frame = []
    fps_stats = FpsStats()
    last_dimensions = {}
    total_objects_detected = 0

    next_objects_event = threading.Event()
    pause_event = threading.Event()

    def __init__(self, camera):
        Recognition.camera = camera
        if Recognition.thread is None:
            Recognition.thread = threading.Thread(target=self._thread)
            Recognition.thread.start()

    def get_objects(self):
        return Recognition.last_objects_seen

    def get_next_objects(self):
        Recognition.next_objects_event.wait()
        Recognition.next_objects_event.clear()
        return self.get_objects()

    def augment_frame(self, frame):
        # Display the results
        for face in self.get_objects():
            name = face["name"]
            top, right, bottom, left = face["aabb"]
            color = (0, 0, 255)

            if name != 'unknown':
                color = (255, 0, 0)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top),
                          (right, bottom), color, 2)

            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        .4, color, 1)
        return frame

    def pause(self):
        Recognition.pause_event.clear()

    def resume(self):
        Recognition.pause_event.set()

    @classmethod
    def stats(cls):
        return {
            "lastDimensions": cls.last_dimensions,
            "fps": cls.fps_stats.stats(),
            "total_objects_detected": cls.total_objects_detected
        }

    @classmethod
    def _thread(cls):
        logger.info('Starting pytorch thread.')
        cls.fps_stats.start()

        # start running on start
        cls.pause_event.set()

        while True:
            cls.pause_event.wait()
            # get frame, run face detection on it and update Recognition.last_objects_seen
            frame = cls.last_frame = cls.camera.get_frame()

            new_objects = []

            # TODO : invoke pytorch magic here
            # new_objects = face_recognition.face_locations(frame)
            #

            cls.last_objects_seen = new_objects

            cls.fps_stats.increment()

            cls.last_dimensions = cls.last_frame.shape

            num_objects = len(cls.last_objects_seen)
            cls.next_objects_event.set()  # send signal to clients
            cls.total_objects_detected += num_objects

            time.sleep(0)
