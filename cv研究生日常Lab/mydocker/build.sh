#!/usr/bin/env bash
apt-get update

# https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh

apt-get install -y python3-pip

pip3 install -r /tmp/requirements.txt

# pip install pytorch or tensorflow here~
# https://pytorch.org/get-started/previous-versions/
# or
# conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch #指明cuda版本即可
pip3 install tensorflow
