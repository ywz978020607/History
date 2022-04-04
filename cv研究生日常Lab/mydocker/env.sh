#!/usr/bin/env bash
if [ x$1 != x ];then
    export COMPOSE_PROJECT_NAME=$1;
else
    project_path=$(pwd);
    project_name="${project_path##*/}";
    export COMPOSE_PROJECT_NAME=$project_name;
fi

alias build="docker-compose build"
# TODO: 使用脚本，包括初次使用，退出-继续运行/停止，重入等
# alias start="docker-compose up -d"
# alias debug="docker-compose up"
alias siteroot="docker-compose run --rm --service-port ldl bash"

alias site="docker-compose run -u $(id -u):$(id -g) --rm --service-port ldl bash"
alias attach="docker attach ${COMPOSE_PROJECT_NAME}_ldl_run_1"
alias once="docker exec -it ${COMPOSE_PROJECT_NAME}_ldl_run_1 /bin/bash"