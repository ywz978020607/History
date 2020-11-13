## 查看当前目录下的文件个数：

ls -l ./|grep "^-"|wc -l



## 查看当前目录占用空间总大小

du -h --max-depth=0



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
2.  res = subprocess.Popen('uptime',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
3. result = res.stdout.readlines()





# 实时查看显卡状态

watch -n 1 -d nvidia-smi



# 取消终端自动弹出无用信息(hyy)

mesg n



# wget

wget -r -np -nd http://example.com/packages/  #`-np` 的作用是不遍历父目录，`-nd` 表示不在本机重新创建目录结构。

#`-c` 选项的作用为断点续传。

#`--accept=iso` 选项，这指示 wget 仅下载 i386 目录中所有扩展名为 iso 的文件

