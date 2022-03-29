#!/usr/bin/env bash

alias build="docker-compose build"

alias start="docker-compose up -d"
alias debug="docker-compose up"

alias site="docker-compose run --rm --service-port ywz_cuda11_1 bash"
