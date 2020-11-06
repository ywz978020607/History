## 查看当前目录下的文件个数：

ls -l ./|grep "^-"|wc -l



## 查看当前目录占用空间总大小

du -h --max-depth=0



## 根据PID查找用户

ps -f -p  PID_Num



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