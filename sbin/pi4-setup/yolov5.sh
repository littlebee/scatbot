#!/bin/bash

#  we are using a custom fork that allows detect(view_img=false) to work for headless
#  and maybe other changes see commits to that repo
git clone https://github.com/littlebee/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ..
