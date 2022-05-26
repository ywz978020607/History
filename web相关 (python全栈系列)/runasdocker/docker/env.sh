#!/usr/bin/env bash

alias build="docker-compose build"

alias start="docker-compose up -d"
alias debug="docker-compose up"

# alias site="docker-compose run --rm --service-port web bash"
alias site="docker-compose run --service-port web bash"

