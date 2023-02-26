#!/bin/bash

# this script is meant to be run from your local development machine,
# in the scatbot project root dir


if [ "$1" == "" ]; then
  echo "Error: missing parameter.  usage: sbin/upload.sh [USER@]IP_ADDRESS_OR_NAME"
  echo "   ex:  sbin/upload.sh pi@scatbot.local"
  exit 1
fi

targetUser=bee
if [ "$2" != "" ]; then
  targetUser=$2
  echo "got user"
  echo $targetUser
fi

# echo on
set -x

# stop on errors
set -e

TARGET_DIR="/home/$targetUser/scatbot"
TARGET_HOST=$1

rsync --progress --partial \
--exclude=node_modules \
--exclude=data/ \
--exclude=.git -avz \
--exclude=yolov5 \
--exclude=debug/commons \
--exclude=camera_test_output.avi \
--exclude=__pycache__/ \
. $TARGET_HOST:$TARGET_DIR
