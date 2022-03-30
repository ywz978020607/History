
# *.docker改造目的
- 保证数据安全性
- 快速支持多版本cuda
- 支持跨机器环境迁移
- 方便管理和用户隔离

# 1.用户操作

不同cuda的docker版本和拉取链接参考  
https://hub.docker.com/r/nvidia/cuda/tags


```
（可选）推荐在Dockefile-编译镜像不执行build.sh以最小化镜像, 在进入容器后手动执行sh /tmp/build.sh  

修改Dockefile基础镜像名字、.yml文件的生成镜像名、挂载本机对应的路径名等信息后
. env.sh
build
#运行容器-见env.sh封装
start/debug/site  

sh /tmp/build.sh #在此处进行环境搭建，最小化镜像

#重新连接  
docker attach [CONTAINER_NAME or CONTAINER_ID]
#热芝士:退出时，使用[ctrl + D]，这样会结束docker当前线程，容器结束，可以使用[ctrl + P][ctrl + Q]退出而不终止容器运行
```

- 迁移docker-兼容性较好，可打包镜像直接迁到其他机器运行容器
```
#如果替换可以不输[:标签]
docker commit -m="描述信息" -a="username" 容器名称|容器ID 生成的镜像名[:标签名]
docker save -o savePathName_xxx.tar 镜像名[:标签] 
docker load -i xxxx.tar
```

# 2.配置完整过程，非管理员可忽略  
## 宿主机安装
显卡驱动装最新版本，不需要管cuda和cudnn  
安装好docker,之后安装nvidia-docker和docker-compose  
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
#接下来在您的主机上安装nvidia-docker2软件包：
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo apt-get install -y docker-compose
```
之后修改sudo vim /etc/docker/daemon.json 
```
sudo vim /etc/docker/daemon.json 
#
{
"default-runtime": "nvidia"  #添加这一句
"runtimes": {
   "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
   }
}
}
#
# 重启docker服务即可生效
sudo systemctl daemon-reload
sudo systemctl restart docker
```


## docker命令权限设置
1、需要先允许所有人执行docker命令  
sudo groupadd docker  
2、把用户添加进docker组中  
sudo gpasswd -a ${USER} docker  
3、重启docker  
sudo service docker restart  
4、如果普通用户执行docker命令，如果提示get …… dial unix /var/run/docker.sock权限不够，则修改/var/run/docker.sock权限
使用root用户执行如下命令，即可
sudo chmod a+rw /var/run/docker.sock #恢复则刷660