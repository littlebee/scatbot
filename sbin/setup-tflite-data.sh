#!/bin/bash

# echo on
set -x

# stop on errors
set -e

DATA_DIR="./data"
TFLITE_DATA_DIR="$DATA_DIR/tflite"

mkdir -p $TFLITE_DATA_DIR

# Download TF Lite models
FILE=${TFLITE_DATA_DIR}/efficientdet_lite0.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1?lite-format=tflite' \
    -o ${FILE}
fi

FILE=${TFLITE_DATA_DIR}/efficientdet_lite0_edgetpu.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/edgetpu/efficientdet_lite0_edgetpu_metadata.tflite' \
    -o ${FILE}
fi

# Models from https://coral.ai/models/object-detection/
# WE WANT THESE!  winner winner chicken dinner of the shootout so far
FILE=${TFLITE_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v1_coco_quant_postprocess.tflite' \
    -o ${FILE}
fi

FILE=${TFLITE_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite' \
    -o ${FILE}
fi
