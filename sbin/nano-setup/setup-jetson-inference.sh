#!/bin/bash

#
# this is from the link below:
# https://github.com/dusty-nv/jetson-inference
#
# Tested on jp46 (jetpack 4.6)

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


sudo apt-get install -y git cmake
sudo apt-get install -y libpython3-dev python3-numpy

cd ~
git clone https://github.com/dusty-nv/jetson-inference
cd jetson-inference
git submodule update --init

set +x
echo "In the build setup that follows, be sure to install the python3 version of PyTorch"
set -x
read -p "Press enter to continue"

mkdir build
cd build
cmake ../

make
sudo make install
sudo ldconfig

set +x
echo "After rebooting, check by doing the following commands:"
echo ""
echo "cd jetson-inference/build/aarch64/bin"
echo "./imagenet.py images/orange_0.jpg ~/inference_test.jpg"
echo ""
echo "It take a couple of minutes on the first run to optimize"
echo "the model / network.  When finished, scp the image local"
echo "and verify"

# see also for verification:
# https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-console-2.md
