#!/bin/bash

# echo on
set -x

# stop on errors
set -e

# custom scatbot stuff
# web and web socket server - https://gitlab.com/pgjones/quart
sudo pip3 install \
quart \
websockets \
flask \
flask-cors

# :heart: PyTorch!  This is the easiest setup ever
#
# This was test with very fresh and clean Raspian Bullseye 64 OS install.
# PyTorch requires a 64 bit os.  It and OpenCV are both included in the
# Bullseye distro.

sudo pip3 install torch torchvision torchaudio
sudo pip3 install opencv-contrib-python
sudo pip3 install numpy --upgrade


# you have to have tried installing tensorflow + opencv to really
# appreciate how easy that was

# Install Adafruit Brainhat accessories
# https://learn.adafruit.com/adafruit-braincraft-hat-easy-machine-learning-for-raspberry-pi/blinka-setup

# Blinka
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py

# reboots

# dot star, motor kit and app libs
sudo pip3 install --upgrade adafruit-circuitpython-dotstar adafruit-circuitpython-motor adafruit-circuitpython-bmp280
sudo pip3 install adafruit-circuitpython-motorkit

# audio
cd ~
sudo apt-get install -y git
git clone https://github.com/HinTak/seeed-voicecard
cd seeed-voicecard
git checkout v5.9
sudo ./install.sh
set +x
echo "Be sure to run raspi-config and under System Options / Audio, "
echo "select bcm2835-i2s-wm8960-hifi"
set -x
speaker-test -c2

sudo apt-get -y install libportaudio2
sudo apt-get -y install portaudio19-dev python3-pyaudio
sudo pip3 install pyaudio


cd ~
sudo pip3 install --upgrade adafruit-python-shell click
sudo apt-get install -y git
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py -u /home/bee --display=st7789_240x240 --rotation=0 --install-type=fbcp

# current sensor lib
sudo pip3 install adafruit-circuitpython-ina219

# install yolo v5
#   https://www.section.io/engineering-education/object-detection-with-yolov5-and-pytorch/
cd src
#  we are using a custom fork that allows detect(view_img=false) to work for headless
#  and maybe other changes see commits to that repo
git clone https://github.com/littlebee/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ../..


set +x
echo "See the link below to test / adjust audio after reboot. "
echo "https://learn.adafruit.com/adafruit-braincraft-hat-easy-machine-learning-for-raspberry-pi/audio-setup"
echo ""
echo "You may need to run sudo raspi-config after rebooting and change:"
echo " - boot loader - to not load GNU desktop "
echo " - fan config - should be on pin 4 and set to 70c"
echo " - interfaces / legacy camera support = yes"
echo ""
echo "And finally, after rebooting, run the following script(s):"
echo " - sbin/setup-display.sh"

read -p "Press any key to continue rebooting"
sudo reboot
