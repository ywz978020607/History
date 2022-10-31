#!/bin/bash
# . autogit.sh

# 获取更新当前分支变量
# temp_branch=$(git symbolic-ref -q --short HEAD)
# echo $temp_branch

# 自动更新主分支并合并到本分支
gmerge(){
    temp_branch=$(git symbolic-ref -q --short HEAD) && echo $temp_branch && git checkout master && git pull origin master && git checkout $temp_branch && git merge master && echo $temp_branch;
}

# 自动推送到远程本分支
gpush(){
    temp_branch=$(git symbolic-ref -q --short HEAD) && echo $temp_branch && git push origin $temp_branch
}

alias gaddup="git add -A && git commit -m 'up'"

# 注：如果使用alias，对于$temp_branch无法动态更新，需要重新alias，使用函数代替
