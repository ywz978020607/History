#!/bin/bash

#mqtt
# python django1/mqtt.py  > docker/log/mqtt.log 2>&1 &

#django
python django1/manage.py runserver 0.0.0.0:8000 > docker/log/django.log 2>&1