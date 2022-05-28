#!/usr/bin/env bash
#换源
sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
apt clean
apt-get update -y

apt-get install -y sudo ssh git gcc g++ make tmux vim net-tools
apt-get install -y libsm6 libxext6 libxrender-dev
# wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh

apt-get install -y python3-pip

pip3 install -r /tmp/requirements.txt

###
# pip install pytorch or tensorflow here~
# https://pytorch.org/get-started/previous-versions/
# or
# conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
# pip3 install tensorflow
