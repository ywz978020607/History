#!/usr/bin/env bash

apt-get update -y
apt-get -y install sshpass
pip3 install -r /tmp/requirements.txt


# export PATH = xx