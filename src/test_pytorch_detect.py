#!/usr/bin/env python3

# stolen from https://github.com/spmallick/learnopencv/tree/master/PyTorch-faster-RCNN
# import necessary libraries
import cv2
import sys
import time


from commons import constants
from vision.pytorch_detect import PytorchDetect

detector = PytorchDetect()


def main(source=constants.CAMERA_CHANNEL_RGB):

    print(f"starting video capture. source={source}")
    video = cv2.VideoCapture(source)

    # We need to check if camera is opened previously or not
    if (video.isOpened() == False):
        print("Error creating video capture")

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)

    frames = 0
    while True:
        # read frame
        ret, image = video.read()
        if not ret:
            raise RuntimeError(f"failed to read frame. ret={ret}")

        t1 = time.time()
        detected_objects = detector.get_prediction(image)
        t2 = time.time()
        frames += 1

        print(f"{frames}: ({t2 - t1}s) {detected_objects} ")


if __name__ == "__main__":
    source = int(sys.argv[1]) if len(
        sys.argv) > 1 else constants.CAMERA_CHANNEL_RGB
    main(source)
