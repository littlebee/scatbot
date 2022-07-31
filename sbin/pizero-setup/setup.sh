#!/bin/bash

# echo on
set -x
# stop on errors
set -e

# for Raspian Bullseye

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

sudo apt install -y \
git \
cmake \
libssl-dev \
libx11-dev \
xorg-dev \
libglu1-mesa-dev \
libusb-1.0-0-dev

# 32 bit only
# sudo apt-get install gcc-7 g++-7
# sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7
# sudo update-alternatives --set gcc "/usr/bin/gcc-7"

# backup swapfile settings and script
TMPDIR=/tmp/scatbot-setup
if [ ! -d $TMPDIR ]; then
  # only if we've never been run
  mkdir -p $TMPDIR/etc
  sudo cp /etc/dphys-swapfile $TMPDIR/etc
fi

# enlarge the swap file for building
sudo cp sbin/pizero-setup/files/etc/dphys-swapfile /etc
sudo /etc/init.d/dphys-swapfile restart swapon -s

git clone https://github.com/IntelRealSense/librealsense.git

cd librealsense/
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger

mkdir build && cd build
# 32 bit
cmake \
-DCMAKE_BUILD_TYPE=RELEASE \
-DBUILD_SHARED_LIBS=false \
-DBUILD_PYTHON_BINDINGS=true \
-DPYTHON_INCLUDE_DIR=/usr/include/python3.9 \
-DPYTHON_EXECUTABLE=/usr/bin/python3.9 \
-DPYTHON_LIBRARY=/usr/lib/python3.9/config-3.9-arm-linux-gnueabihf/libpython3.9.so \
..

# 64 bit
# cmake \
# -DCMAKE_BUILD_TYPE=RELEASE \
# -DBUILD_SHARED_LIBS=false \
# -DBUILD_PYTHON_BINDINGS=true \
# -DPYTHON_INCLUDE_DIR=/usr/include/python3.9 \
# -DPYTHON_EXECUTABLE=/usr/bin/python3.9 \
# -DPYTHON_LIBRARY=/usr/lib/python3.9/config-3.9-aarch64-linux-gnu/libpython3.9.so \
# ..


make
sudo make install

# custom scatbot stuff
# web and web socket server

# opencv (below) is used to compress images to jpeg for web streaming
# these additional packages are needed for opencv:
sudo apt-get install -y \
python3-h5py \
libopenjp2-7 \
ffmpeg \
libatlas-base-dev

sudo apt install -y python3-pip

sudo pip3 install \
websockets \
flask \
flask-cors \
opencv-contrib-python-headless


read -p "Press any key to continue rebooting"
sudo reboot
