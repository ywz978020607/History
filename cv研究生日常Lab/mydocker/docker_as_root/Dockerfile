FROM nvidia/cuda:11.3.0-devel-ubuntu18.04
ENV PYTHONUNBUFFERED 1
ENV NVIDIA_VISIBLE_DEVICES ALL
ADD . /tmp
# RUN sh /tmp/build.sh

#--处理用户名uid一致性且支持迁移---
#RUN apt-get update && apt-get install -y sudo \
#&& useradd --create-home --no-log-init --shell /bin/bash docker \
#&& adduser docker sudo \
#&& echo 'docker:123456' | chpasswd \
#&& usermod -a -G adm docker && usermod -a -G sudo docker

# 安装配置 fixuid
#RUN USER=docker && \
#    GROUP=docker && \
#    cp /tmp/fixuid /usr/local/bin/ && \
#    chown root:root /usr/local/bin/fixuid && \
#    chmod 4755 /usr/local/bin/fixuid && \
#    chmod +x /tmp/entrypoint.sh && \
#    mkdir -p /etc/fixuid && \
#    printf "user: $USER\ngroup: $GROUP\npaths:\n  - /home/docker\n" > /etc/fixuid/config.yml

#USER docker:docker

#ENTRYPOINT ["/tmp/entrypoint.sh"]
# ENTRYPOINT ["fixuid"]
#--处理uid一致性且支持迁移--done---


# RUN mkdir /src
