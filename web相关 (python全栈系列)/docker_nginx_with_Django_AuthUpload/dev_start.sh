#!/bin/bash

python django1/manage.py runserver 0.0.0.0:8000 > docker/log/django.log 2>&1