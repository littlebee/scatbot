#!/bin/bash

# This is from:
#  https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/initial-setup

# echo on
set -x

# stop on errors
set -e


# Set your Python install to Python 3 Default
sudo apt install -y python3 git python3-pip
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
sudo update-alternatives --config python

# Install Python 3.7 and Make Default
sudo apt install -y python3.7-dev
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
sudo update-alternatives --config python

# Upgrade your board
sudo apt update
sudo apt upgrade

# Update all python packages
pip3 freeze - local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
# and global packages too
sudo bash -c "pip3 freeze - local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U"

# set user permissions
sudo groupadd -f -r gpio
sudo usermod -a -G gpio pi
cd ~
git clone https://github.com/NVIDIA/jetson-gpio.git
sudo cp ~/jetson-gpio/lib/python/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d

# install python libs
sudo pip3 install adafruit-blinka



set +x
echo "new python version: $(python --version)"
echo ""
echo "you need to run 'sudo /opt/nvidia/jetson-io/jetson-io.py' and enable SPI"
echo "see, https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/initial-setup#enable-uart-i2c-and-spi-3039597-23"
echo ""

