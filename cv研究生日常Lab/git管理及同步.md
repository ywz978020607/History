1. github注册仓库获得链接

2. 文件夹中打开bash

   git init

   git add -A

   git commit -m "up"

   git remote  add origin  https://github.com/ywz978020607/phddns_arm64_or_others_onenet.git

   git push origin master  # -f #强制push

------------------------

github使用本地翻墙socks代理

git config --global http.https://github.com.proxy socks5://127.0.0.1:10808

git config --global https.https://github.com.proxy socks5://127.0.0.1:10808



取消代理

git config --global --unset http.proxy 

git config --global --unset https.proxy  



查看已有配置

git config --global -l 

删除本地分支所有修改，同步远程 master 到本地，使用 git reset --hard origin/master

## 忽略本地修改，强拉

```
git fetch --all

git reset --hard origin/dev

git pull
```

## prune--解决pull报错问题
使用git pull拉取代码的时候，无法拉取最新代码，报"unable to update local ref"错误。

除了重新clone一份代码外，还可以使用如下解决方案：
1、切换到之前clone代码目录下，执行命令
2、再执行命令
3、再次使用
```
git gc --prune=now
git remote prune origin
git pull
```

## 查看所有分支

git branch

## 多机同步流程
先git clone

创建本地分支
git checkout -b "dev"

将本地当前分支推到远端dev分支
git push origin dev

将本地分支关联远端dev分支
git branch --set-upstream-to=origin/dev

git pull

查看当前关联分支
git remote -v


## master修改内容后更新到各个分支
本机仍然有一个master分支 用来时刻与主master保持同步
git checkout master
git pull

再切换到本地分支下
git checkout dev

合并master到dev(当前)
git merge master

再将合并后的本地分支提交到云端分支
git push 
git push origin dev

## 分支汇入master(管理员)
同上 merge时使用
git merge dev
再提交即可