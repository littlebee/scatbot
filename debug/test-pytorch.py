#!/usr/bin/env python3

# this is from https://pytorch.org/tutorials/intermediate/realtime_rpi.html

import time
from os.path import exists

from commons import constants

# OMG, only python and nano, you HAVE to import cv2
#  before torch on nano.
#  https://github.com/opencv/opencv/issues/14884#issuecomment-599852128
import cv2

import torch
import numpy as np
from torchvision import models, transforms


is_jetson = exists('/etc/nv_tegra_release')

#  This doesn't work on nano
if not is_jetson:
    torch.backends.quantized.engine = 'qnnpack'

cap = None
# TODO : figure out someway to import commons/constants
cap = cv2.VideoCapture(constants.CAMERA_CHANNEL_RGB, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

print("loading model")
net = None
if is_jetson:
    net = models.quantization.mobilenet_v2(pretrained=True)
else:
    # This also doesn't work on nano :/
    net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)

print("compiling model")
net = torch.jit.script(net)

print('model compiled')
started = time.time()
last_logged = time.time()
frame_count = 0

with torch.no_grad():
    print("starting benchmark")
    while True:
        # read frame
        ret, image = cap.read()
        if not ret:
            raise RuntimeError(f"failed to read frame. ret={ret}")

        # convert opencv output from BGR to RGB
        image = image[:, :, [2, 1, 0]]
        permuted = image

        # preprocess
        input_tensor = preprocess(image)

        # create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # run model
        output = net(input_batch)
        # do something with output ...

        # print(f"{output}")

        # log model performance
        frame_count += 1
        now = time.time()
        if now - last_logged > 1:
            print(f"{frame_count / (now-last_logged)} fps")
            last_logged = now
            frame_count = 0
