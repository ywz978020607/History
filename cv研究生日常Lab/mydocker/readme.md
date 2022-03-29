
# 1.用户操作
```
查看mydocker/build.sh 填补需要的命令和修改对应的路径名等信息
. env.sh
build
#运行容器-见env.sh封装
start/debug/site
```


# 2.配置完整过程，非管理员可忽略  
## 宿主机安装
显卡驱动装最新版本，不需要管cuda和cudnn  
安装好docker,之后安装nvidia-docker和docker-compose  
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
接下来在您的主机上安装nvidia-docker2软件包：
apt-get update
apt-get install -y nvidia-docker2
apt-get install -y docker-compose
```

不同cuda的docker版本和拉取链接参考  
https://hub.docker.com/r/nvidia/cuda/tags

## docker命令权限设置
1、需要先允许所有人执行docker命令  
sudo groupadd docker  
2、把用户添加进docker组中  
sudo gpasswd -a ${USER} docker  
3、重启docker  
sudo service docker restart  
4、如果普通用户执行docker命令，如果提示get …… dial unix /var/run/docker.sock权限不够，则修改/var/run/docker.sock权限
使用root用户执行如下命令，即可
sudo chmod a+rw /var/run/docker.sock
