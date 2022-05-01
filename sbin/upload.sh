#!/bin/bash

# this script is meant to be run from your local development machine.


if [ "$1" == "" ]; then
  echo "Error: missing parameter.  usage: sbin/upload.sh [USER@]IP_ADDRESS_OR_NAME"
  echo "   ex:  sbin/upload.sh pi@raspberrypi.local"
  exit 1
fi

# echo on
set -x

# stop on errors
set -e

TARGET_DIR="/home/bee/scatbot"
TARGET_HOST=$1

rsync --progress --partial --exclude=node_modules --exclude=data/ --exclude=.git -avz . $TARGET_HOST:$TARGET_DIR

