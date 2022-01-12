## [git可视化练习网站](http://git-school.github.io/visualizing-git/)

## 快速拉取--只拉取某个分支的某个版本
```
git clone --single-branch -b <分支名> --depth 1 http://your-site.com/your-group/your-repo.git
```

## 将现有的一个文件夹强制提交到git仓库

```
1. github注册仓库获得链接
2. 文件夹中打开bash

   git init

   git add -A

   git commit -m "up"

   git remote  add origin  https://github.com/ywz978020607/phddns_arm64_or_others_onenet.git

   git push origin master  # -f #强制push
```

## 配置git及多环境

https://juejin.cn/post/6844904180633600007

```bash
ssh-keygen -t rsa -f ~/.ssh/id_rsa.gitee -C "你的邮箱"

#ssh-agent bash
#ssh-add ~/.ssh/id_rsa.github
#ssh-add ~/.ssh/id_rsa.gitee

#~/.ssh/config
# gitee
Host gitee.com
HostName gitee.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa.gitee

# github
Host github.com
HostName github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa.github
ProxyCommand connect -S 127.0.0.1:10808 -a none %h %p #win-dns解析失败时设置走本机socks代理
####################

#test in cmd-shell
ssh -T git@github.com
```

## 一个工程项目同时推送github和gitee两个平台

```
   1. 机器需要配置两组密钥 并在~/.ssh/config文件中添加
      # gitee
      Host gitee.com
      HostName gitee.com
      PreferredAuthentications publickey
      IdentityFile ~/.ssh/id_rsa.gitee

      # github
      Host github.com
      HostName github.com
      PreferredAuthentications publickey
      IdentityFile ~/.ssh/id_rsa.github
      #ProxyCommand connect -S 127.0.0.1:10808 -a none %h %p #win-dns解析失败时设置走本机socks代理

   2. 在正常配置一个git项目内
      git remote set-url --add origin xxxx
      或修改.git/config中的origin中新增一行
      url = git@gitee.com:xxxxx 
```

## github使用本地翻墙socks代理 -- 不推荐，建议在ssh-config添加代理

```
git config --global http.https://github.com.proxy socks5://127.0.0.1:10808

git config --global https.https://github.com.proxy socks5://127.0.0.1:10808


取消代理

git config --global --unset http.proxy 

git config --global --unset https.proxy  



查看已有配置

git config --global -l 
```

## 删除本地分支所有修改，同步远程 master 到本地，

`使用 git reset --hard origin/master`

## rebase -常用

无法拉也无法推时

```git
git pull origin xxx --rebase   #xxx为分支名
```

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

## 拉取远程的某分支并创建本地对应新分支
```
git fetch origin dev:dev
```

## 查看所有分支

`git branch`

## 多机同步流程

```
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
```

## master修改内容后更新到各个分支

```
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
```

## 分支汇入master(管理员)

```
同上 merge时使用
git merge dev
再提交即可
```



## 合并策略

*send->合到reveive分支*

1. 直接merge -- 会有岔路

```
git checkout receive
git merge send
```

2. 使用rebase -- 完全线性记录

   ```
   git checkout send

   #将本分支send分支更改续到receive后:完全线性,如果需要冲突默认策略,可以在rebase后加参数-X theirs等
   git rebase receive

   git checkout receive
   git merge send
   ```

   - 冲突时 -- vim删除当前行快捷键 `dd`
   - git pull = fetch + merge

## 回滚提交

1. 恢复到某一次的提交 git reset


## 设定.gitignore
重置git状态  
```
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```  

设定ignore规则  
```
#.gitignore
# 忽略所有文件
*
# 不忽略目录
!*/
# 不忽略文件.gitignore和*.foo
!.gitignore
!*.foo
```
