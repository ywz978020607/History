## 控制台输出同时输出日志
`<command> 2>&1 | tee <logfile>`
加入-a参数表示追加  
## 仅输出到日志
`<command> 2>&1 >/dev/null | tee logfile`
加入-a参数表示追加  

## 打印时间
date +%Y%m%d-%H:%M:%S  

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
# alias用法
可以在sh文件中设置alias别名  
`alias s509=""ssh ywz@10.134.xxxx -J ywz@4678xxxx:32xxx""`  
执行. env.sh后 即可在shell中执行s509  
打印查看别名： `type s509` 或 `alias s509`  

# scp+跳板机
方法一：通过ssh -N -L 将远程端口转发到本机，再进行scp  
```bash
HostA(本机)$ ssh -L 0.0.0.0:PortA:HostC:PortC  user@HostB -p port
```  
这时访问 HostA:PortA 相当于访问 HostC:PortC。  
例如：`ssh -L 0.0.0.0:9000:10.130.159.113:22 ywz@467830y6j3.zicp.vip -p 32027`  

方法二：scp+进行跳板机命令，以本地文件$local_path上传到远程为例  
`scp -o ProxyCommand='ssh -q 用户名@A.A.A.A -W %h:%p' helloWord-1.0-SNAPSHOT.jar 用户名@B.B.B.B:/home/worker/`  
用户名@A.A.A.A : ssh 登录relay是的用户名和relay机器地址  
用户名@B.B.B.B : scp 到目标服务器的用户名和服务器地址  


# 走win的代理
export ALL_PROXY=socks5://10.136.150.144:10808
curl cip.cc #测试
unset ALL_PROXY #取消代理

# 默认开机开启/关闭图形界面
#临时方式可以用init 3/5 #cmd/UI
#默认下次开机后cmd
sudo systemctl set-default multi-user.target
#默认下次开机后UI
sudo systemctl set-default graphical.target