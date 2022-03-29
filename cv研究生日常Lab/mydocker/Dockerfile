FROM nvidia/cuda:10.2-base-ubuntu18.04
ENV PYTHONUNBUFFERED 1
ADD . /tmp
RUN sh /tmp/build.sh
# RUN pip install -r /tmp/requirements.txt
RUN mkdir /src
WORKDIR /src
