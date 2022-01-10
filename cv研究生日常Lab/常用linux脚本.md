## 查看当前目录下的文件个数：

ls -l ./|grep "^-"|wc -l

## 查看当前目录占用空间总大小

du -h --max-depth=0

## 查看用户占用空间

sudo du -sh /home/*

## 根据PID查找用户

ps -f -p  PID_Num

# 查询端口进程

lsof -i:xxx

netstat -tunlp|grep 端口号

## 杀死进程

kill PID_Num

# 获取输出

1. import os
2. p = os.popen('uptime')
3. x=p.read()
4. print x

##### 

1. import subprocess
2. res = subprocess.Popen('uptime',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
3. result = res.stdout.readlines()

# 实时查看显卡状态

watch -n 1 -d nvidia-smi

# 取消终端自动弹出无用信息(hyy)

mesg n

可以添加在~/.profile里

# wget

wget -r -np -nd http://example.com/packages/  #`-np` 的作用是不遍历父目录，`-nd` 表示不在本机重新创建目录结构。

#`-c` 选项的作用为断点续传。

#`--accept=iso` 选项，这指示 wget 仅下载 i386 目录中所有扩展名为 iso 的文件

# scp

scp -r filepath user@10.134.xxx:/home/user/path

# sudo users

更改文件夹所属：

```
chown -R username:users Document/
```

https://www.cnblogs.com/vincedotnet/p/4017574.html

cat /etc/passwd

cat /etc/group

\3. 修改用户的密码

sudo passwd wyx

\4. 删除一个用户

sudo userdel wyx

\5. 为该用户添加sudo权限

sudo usermod -a -G adm ywz

sudo usermod -a -G sudo ywz

# 设置默认文件夹位置

vim  /etc/passwd

找到用户对应的行，将文件路径修改即可

-R 可选 ： 高层级低权限即可

修改文件夹所属用户

chown username:username  /home/user_dir

并赋权限700  （-R可选)

chmod 700 /home/user_dir

或批量赋值  chmod 700 xxx/* #所有子文件夹

# 查看当前文件夹下各文件夹的大小

du --max-depth=1 -h

df -h

# 监控文件输出--高级版cat
添加-f后为循环读取  
tail -n 尾部行数 -f 文件名  
eg  tail -f -n 20 temp.log 或  tail -n 20 -f temp.log

tailf 等同于tail -f -n 10

# grep

关键词查询  `xxxx | grep keywords`  
反向选择  `grep -v keywords`  
找出关键词相邻的10行   `tail -n 50 temp.log | grep "ERROR" -C 10`  


# supervisor不正常启动

```
ps ax | grep supervisord
kill -9 PID号   结束进程
supervisorctl reload #最后重新载入配置
```
