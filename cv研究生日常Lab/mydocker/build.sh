#!/usr/bin/env bash
apt-get update
apt-get install -y python3-pip

pip3 install -r /tmp/requirements.txt

# pip install pytorch or tensorflow here~
pip3 install tensorflow
