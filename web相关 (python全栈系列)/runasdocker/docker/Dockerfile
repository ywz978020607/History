FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD . /tmp
# RUN pip install -r /tmp/requirements.txt
RUN sh /tmp/build.sh
RUN mkdir /src
WORKDIR /src
