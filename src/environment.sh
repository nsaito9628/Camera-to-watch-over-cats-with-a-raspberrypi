#!/bin/bash

sudo apt update  
sudo apt -y upgrade  
python3 -m pip install --upgrade pip  
sudo apt install -y postfix git docker awscli
sudo apt install libatlas-base-dev libjasper-dev
sudo apt install ffmpeg  libcanberra-gtk3-module v4l-utils qv4l2 -y
pip3 install awscli aws-sam-cli boto3 --upgrade
python3 -m pip install opencv-python==4.5.4.60


cd /usr/bin
sudo rm python
sudo ln -s python3 python
cd