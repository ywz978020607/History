#!/bin/bash
# . autogit.sh

# 获取更新当前分支变量
# temp_branch=$(git symbolic-ref -q --short HEAD)
# echo $temp_branch

# 自动更新主分支并合并到本分支
alias gmerge="temp_branch=$(git symbolic-ref -q --short HEAD) && git checkout master && git pull origin master && git checkout $temp_branch && git merge master && git branch | grep '*'"

#
alias gaddup="git add -A && git commit -m 'up'"
alias gpush="temp_branch=$(git symbolic-ref -q --short HEAD) && git push origin $temp_branch"


