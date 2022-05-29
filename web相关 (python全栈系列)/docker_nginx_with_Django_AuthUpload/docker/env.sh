#!/usr/bin/env bash
# . env 10.134.162.162 xx 467830y6j3.zicp.vip 57009
export gitlabip=$1;
export passwd=$2;
export openip=$3;  #内网穿透
export openport=$4; 

alias build="docker-compose build"

alias start="docker-compose up -d"
alias debug="docker-compose up"

# alias site="docker-compose run --rm --service-port web bash"
alias site="docker-compose run --service-port web bash"

