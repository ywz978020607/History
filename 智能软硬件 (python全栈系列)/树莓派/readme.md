# 图形界面与命令行

命令行ssh内切换

sudo init 5 #show #or: sudo startx #show

sudo init 3 #close



## 原生系统版：

烧录后，在boot目录下添加"ssh"文件，自动开启ssh

sudo raspi-config
boot_behavior->关闭boot to desktop 节省内存



还有一些其他配置，然后操作系统就可以用了。

1）一个静态IP让一切变得更容易，切换eth0的网络设置：

\>> sudo nano -w /etc/network/interfaces

更改eth0的那行 iface eth0 inet dhcp ，如下所示（根据你的家庭网络设置修改）：

======/etc/network/interfaces====== ... iface eth0 inet static address 192.168.1.10 netmask 255.255.255.0 gateway 192.168.1.1 ... ======/etc/network/interfaces======

2）创建本地用户并加入到users组和sudo组：

\>> sudo adduser YOURUSERIDHERE >> sudo usermod -a -G users YOURUSERIDHERE >> sudo usermod -a -G sudo YOURUSERIDHERE

3）更新系统确保所有的库是最新最好的：

\>> sudo apt-get update; sudo apt-get upgrade

4）好了，准备重新启动吧！先关闭PI：

\>> sudo /sbin/shutdown -h now



===========================

## 换源

正文
登陆到树莓派。你可以通过屏幕键鼠直接打开终端或者通过putty SSH登陆到树莓派。
备份源文件。执行如下命令：
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/raspi.list /etc/apt/sources.list.d/raspi.list.bak
修改软件更新源，执行如下命令：
sudo nano /etc/apt/sources.list
将第一行修改成中科大的软件源地址，「Ctrl+O」进行保存，然后回车，「Ctrl+X」退出。
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
修改系统更新源，执行如下命令：
sudo nano /etc/apt/sources.list.d/raspi.list
将第一行修改成中科大的系统源地址，「Ctrl+O」进行保存，然后回车，「Ctrl+X」退出。
deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ stretch main ui

sudo apt-get update

sudo apt-get upgrade

=========================================

## python->python3

树莓派自带python2和3版本，要想使用3的话，还得特地敲python3、pip3等等一系列的指令

但是python2我们基本上都已经不学了

#所以删除python2.7，输入：

#sudo apt-get autoremove python2.7
#卸载完后，我们发现想用python3的时候，还得敲python3

想敲python直接出来python3的话，那么先把python链接删掉：

sudo rm /usr/bin/python
载新建一个链接：

sudo ln -s /usr/bin/python3.7 /usr/bin/python
查看版本：

which python

python

============================================

\- 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/ - 阿里云 http://mirrors.aliyun.com/pypi/simple/ - 豆瓣 http://pypi.douban.com/simple/ - 华中理工大学 http://pypi.hustunique.com/simple/ - 山东理工大学 http://pypi.sdutlinux.org/simple/ - 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/ 

如果图省事，建立一个配置文件，一劳永逸：

```bash
$ cd ~
$ mkdir .pip
$ cd .pip
$ nano pip.conf
```

输入：

```
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```

============================================

## 端口开放

### 一、查看iptables是否已安装

```bsh
iptables --version
```

### 二、开启指定端口

```js
# 开启80端口
iptables -I INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
iptables  -I OUTPUT -o eth0 -p tcp --sport 80 -j ACCEPT
```

### 三、关闭指定端口

```bsh
# 关闭80端口
iptables -I INPUT -i eth0 -p tcp --dport 80 -j DROP
iptables -I OUTPUT -o eth0 -p tcp --sport 80 -j DROP
```

-------------------------------------------------------------

或或或或或或：

ufw是一个主机端的iptables类防火墙配置工具，比较容易上手。如果你有一台暴露在外网的树莓派，则可通过这个简单的配置提升安全性。

***\*安装方法\****
**sudo apt-get install ufw**

***\*使用方法\**
1.启用
\**sudo ufw enable
sudo ufw default deny\****
作用：开启了防火墙并随系统启动同时关闭所有外部对本机的访问（本机访问外部正常）。

**2.关闭**
**sudo ufw disable**

**3.查看防火墙状态**
**sudo ufw status**

**4.开启/禁用相应端口**
**sudo ufw allow 80** 允许外部访问80端口
**sudo ufw delete allow 80** 禁止外部访问80 端口

============================================

## mongodb

树莓派安装配置mongodb

https://blog.csdn.net/volatile_scq/article/details/100726551
命令行输入：
sudo apt-get install mongodb-server
等待安装完成

修改配置文件
命令行输入：
sudo nano /etc/mongodb.conf
使局域网内可以访问

使用 # 注释掉
bind_ip = 127.0.0.1
变为
#bind_ip = 127.0.0.1
增加用户密码验证连接

去掉#号注释
#auth = true
变为
auth = true
保存文件退出

增加mongodb用户
命令行依次输入：
1.mongo
2.use admin
3.db.addUser('ywz', 'ywz')
4.quit()
python连接mongodb
使用 pymongo==3.2
命令行输入：
	sudo pip3 install  pymongo==3.2  # 树莓派32位系统必须用3.2，高了不行

#树莓派32位系统数据库支持2G

#######################################

# GPIO python3

> import RPi.GPIO as GPIO

####  改变GPIO模式

> GPIO.setmode(GPIO.BCM)

### 拿2号GPIO做实例 

#### #设置2管脚为输出 

> GPIO.setup(2,GPIO.OUT)

#### #设置GPIO2为高电平

> GPIO.output(2,GPIO.HIGH)

#### #设置GPIO2为低电平

> GPIO.output(2,GPIO.LOW)