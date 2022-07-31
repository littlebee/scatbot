#!/bin/bash

#
# this is from the link below:
# https://automaticaddison.com/how-to-install-opencv-4-5-on-nvidia-jetson-nano/
#
# Tested on jp46 (jetson-nano-jp461-sd-card-image.zip) build from this image here:
# https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write

if [[ ! -f "/etc/nv_tegra_release" ]]
then
    echo "This script is only for jetson nano."
    echo "/etc/nv_tegra_release does not exist on your filesystem."
    exit 1
fi

# echo on
set -x

# stop on errors
set -e

sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/nvidia-tegra.conf"
sudo ldconfig

APT_INSTALL="sudo apt install -y "

$APT_INSTALL build-essential cmake git unzip pkg-config
$APT_INSTALL libjpeg-dev libpng-dev libtiff-dev
$APT_INSTALL libavcodec-dev libavformat-dev libswscale-dev
$APT_INSTALL libgtk2.0-dev libcanberra-gtk*
$APT_INSTALL python3-dev python3-numpy python3-pip
$APT_INSTALL libxvidcore-dev libx264-dev libgtk-3-dev
$APT_INSTALL libtbb2 libtbb-dev libdc1394-22-dev
$APT_INSTALL libv4l-dev v4l-utils
$APT_INSTALL libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
$APT_INSTALL libavresample-dev libvorbis-dev libxine2-dev
$APT_INSTALL libfaac-dev libmp3lame-dev libtheora-dev
$APT_INSTALL libopencore-amrnb-dev libopencore-amrwb-dev
$APT_INSTALL libopenblas-dev libatlas-base-dev libblas-dev
$APT_INSTALL liblapack-dev libeigen3-dev gfortran
$APT_INSTALL libhdf5-dev protobuf-compiler
$APT_INSTALL libprotobuf-dev libgoogle-glog-dev libgflags-dev


cd ~

if [[ ! -f "/etc/nv_tegra_release" ]]
then
  wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.1.zip
  wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.1.zip
  unzip opencv.zip
  unzip opencv_contrib.zip

  mv opencv-4.5.1 opencv
  mv opencv_contrib-4.5.1 opencv_contrib
  rm opencv.zip
  rm opencv_contrib.zip
fi

cd ~/opencv
mkdir -p build
cd build

cmake \
-DCMAKE_BUILD_TYPE=RELEASE \
-DCMAKE_INSTALL_PREFIX=/usr/local .. \
-DOPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-DEIGEN_INCLUDE_PATH=/usr/include/eigen3 \
-DWITH_OPENCL=OFF \
-DWITH_CUDA=ON \
-DCUDA_ARCH_BIN=5.3 \
-DCUDA_ARCH_PTX="" \
-DWITH_CUDNN=ON \
-DWITH_CUBLAS=ON \
-DENABLE_FAST_MATH=ON \
-DCUDA_FAST_MATH=ON \
-DOPENCV_DNN_CUDA=ON \
-DENABLE_NEON=ON \
-DPYTHON_INCLUDE_DIR=/usr/include/python3.7 \
-DBUILD_NEW_PYTHON_SUPPORT=ON \
-DBUILD_opencv_python3=ON \
-DHAVE_opencv_python3=ON \
-DPYTHON3_EXECUTABLE=/usr/bin/python3.7 \
-DPYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3.7 \
-DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.7m.so \
-DPYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
-DINSTALL_PYTHON_EXAMPLES=ON \
..

make -j4

cd ~
sudo rm -rf /usr/include/opencv4/opencv2

cd ~/opencv/build
sudo make install
sudo ldconfig
sudo apt-get update

set +x
echo "After verifying the above worked, be sure to..."
echo "cd ~/opencv/build && make clean"
echo ""


