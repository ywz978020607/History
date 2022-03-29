#!/usr/bin/env bash

alias build="docker-compose build"


# TODO: 使用脚本，包括初次使用，退出-继续运行/停止，重入等
alias start="docker-compose up -d"
alias debug="docker-compose up"
alias site="docker-compose run --rm --service-port ywz_cuda11_1 bash"
