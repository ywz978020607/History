
# 炼丹炉容器化隔离改造

# 0.改造目的
- 保证数据安全性
- 快速支持多版本cuda
- 支持跨机器环境迁移
- 方便管理和用户隔离
- 概念扫盲:
  - dockerhub基础镜像+dockerfile=>镜像文件image(宿主机存储, 安全)   
  - 镜像文件image + 宿主机路径挂载(实时同步)&docker-compose.yml=>容器container(重启后无状态)
  - container-执行commit=>镜像文件image(宿主机存储)
  - 修改dockerfile需要重新编译build，需改docker-compose.yml不需要重新编译
  - 宿主机不再需要tmux

# 1.用户操作

不同cuda的docker版本和拉取链接参考  
https://hub.docker.com/r/nvidia/cuda/tags

#推荐在Dockefile-编译镜像不执行build.sh以最小化镜像, 在进入容器后手动执行sh /tmp/build.sh, 使用如下  
```
#预处理:
a.根据hub.docker.com找到需要的基础镜像名字，修改Dockefile第一行。
b.根据自己的挂载需要，修改docker-compose.yml的volumes和ports(宿主机:容器) -- 一般挂载一个代码文件和模型文件夹即可
#

. env.sh # 可选加入自定义镜像前缀, eg:. env.sh ywz_cuda11_1 或 . env.sh ywz111
# docker images 查看当前所有镜像
# build # 重新编译构造镜像，谨慎

#初次运行容器-见env.sh封装 
site

#...配置自己的环境，如安装anaconda/pytorch/tensorflow等，如果可以写到build.sh，也可以手动装
sh /tmp/build.sh #在此处进行环境搭建，最小化镜像
#注意:首次配置完成后，一定要运行以下命令
docker commit -m="描述信息" -a="username" 容器名称(或容器ID) 生成的镜像名
#将配置好的容器环境提交并替换个人镜像，之后无论容器/宿主机重启，直接进入容器不需要重新配置环境


#重新连接  
docker ps -a #查看所有容器
docker attach [CONTAINER_NAME or CONTAINER_ID] # 快速命令>attach
#热芝士:退出时，使用[ctrl + D]，这样会结束docker当前线程，容器结束，可以使用[ctrl + P][ctrl + Q]退出而不终止容器运行
or
#新开一个临时bash窗口到容器，结束时ctrl+D/ctrl+P+Q均可，里面需要进tmux跑程序
docker exec -it [CONTAINER_NAME or CONTAINER_ID] /bin/bash #快速命令>once
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
```
sudo apt-get update
sudo apt-get install -y docker.io
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
#接下来在您的主机上安装nvidia-docker2软件包：
sudo apt-get install -y nvidia-docker2
sudo apt-get install -y docker-compose
```
之后修改sudo vim /etc/docker/daemon.json 
```
sudo vim /etc/docker/daemon.json 
#
{
   "default-runtime": "nvidia",  #添加这一句
   "runtimes": {
      "nvidia": {
         "path": "/usr/bin/nvidia-container-runtime", #保持默认不用改
         "runtimeArgs": []
      }
   },
   "registry-mirrors":[], #docker镜像源-可选
   "data-root": "/temp_disk2/dockerdata"   #docker镜像路径
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

```
sudo groupadd docker  
sudo gpasswd -a [ywz/dyf/zyt] docker  
sudo service docker restart  
sudo chmod a+rw /var/run/docker.sock #恢复则刷660
```


## 管理员docker命令
```
docker ps -a
docker ps -a -q
#停止/删除所有容器
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```