#!/bin/bash

set -x
set -e

cd ~/jetson-inference/build/aarch64/bin
./imagenet.py images/orange_0.jpg ~/inference_test.jpg

set +x
echo "you can verify that the inference worked by pulling the "
echo "file local and opening it like: "
echo "   scp scatbot-nano.local:/home/bee/inference_test.jpg . && open inference_test.jpg"
echo ""
