#!/usr/bin/env bash
apt-get update
apt-get install -y ssh git gcc g++ make tmux vim net-tools
apt-get install -y libsm6 libxext6 libxrender-dev
# wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh

apt-get install -y python3-pip

pip3 install -r /tmp/requirements.txt

#--处理用户名uid一致性且支持迁移---
RUN useradd --create-home --no-log-init --shell /bin/bash docker \
&& adduser docker sudo \
&& echo 'docker:123456' | chpasswd \
&& usermod -a -G adm docker && usermod -a -G sudo docker

# 安装配置 fixuid
RUN USER=docker && \
    GROUP=docker && \
    cp /tmp/fixuid /usr/local/bin/ && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\n" > /etc/fixuid/config.yml

USER docker:docker
ENTRYPOINT ["fixuid"]
#--处理uid一致性且支持迁移--done---




# pip install pytorch or tensorflow here~
# https://pytorch.org/get-started/previous-versions/
# or
# conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
# pip3 install tensorflow
