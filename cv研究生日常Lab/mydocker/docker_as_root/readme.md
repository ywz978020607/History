
# 炼丹炉容器化隔离改造 [本目录文件打包下载](https://raw.githubusercontent.com/ywz978020607/History/master/cv%E7%A0%94%E7%A9%B6%E7%94%9F%E6%97%A5%E5%B8%B8Lab/mydocker/mydocker.tar)
```
#pack:
tar cvf mydocker.tar build.sh docker-compose.yml Dockerfile entrypoint.sh env.sh fixuid requirements.txt readme.md
#unpack:
tar xvf mydockr.tar
```

# 0.改造目的
- 保证数据安全性
- 快速支持多版本cuda
- 支持跨机器环境迁移
- 方便管理和用户隔离
- 实现环境/docker/所有数据->机械硬盘/nfs，使得与宿主机的固态硬盘分离，故障时重做系统更加安全、快速恢复
- 概念扫盲:
  - dockerhub基础镜像+dockerfile=>镜像文件image(宿主机存储, 安全)   
  - 镜像文件image + 宿主机路径挂载(实时同步)&docker-compose.yml=>容器container(重启后无状态)
  - container-执行commit=>镜像文件image(宿主机存储)
  - 修改dockerfile需要重新编译build，需改docker-compose.yml不需要重新编译
  - 宿主机不再需要tmux

- 功效：
  - 开发环境优化：Docker（推荐，配置的docker路径也在机械盘，保证安全）
  - 开发流程优化：Git-个人代码分支维护，推荐使用gitee，见内部网站教程
  - 数据安全优化：数据一定存放在/temp_disk2等机械硬盘上
  - 数据一致性优化：NFS（可选，校园网共享某台机器的某块硬盘，见内部网站，可提需求由管理员部署）
  - 机器稳定性优化：每台宿主机只维护系统/网络/显卡驱动(可自动安装)/docker环境/ssh，其他例如cuda版本、cudnn、conda等均不再维护，基本确保机器随时重装系统1小时可全面恢复。

- 补充:
  - 普通docker部署后进入root，宿主机难以追溯真实使用人，为此加入fixuid，容器内统一自动创建使用docker用户，uid会自动绑定调用者的宿主机下账号的uid，uid统一后能够更好实现权限管理和成本追溯等任务
  - 注意仅docker-compose.yml的volumes挂载卷数据是实时同步的，需要个性化配置。也可以参考nfs网络共享配置，将代码/数据集从其他机器上共享，见[nfs网络共享](../nfs网络共享配置/)
  - 显卡驱动装好后输入`nvidia-smi`能看到最高支持的cuda版本，选择基础镜像时选择低于此版本的才能正常构建/迁移，此外，pytorch目前最高支持到11.3，且3090显卡可能不支持cuda10及以下版本，所有通用建议选择cuda11.3版本最佳.

# 1.用户操作

不同cuda的docker版本和拉取链接参考，找合适的-devel-ubuntu版本([区别说明](https://blog.csdn.net/u011622208/article/details/113650011))  
[Nvidia-docker镜像库](https://hub.docker.com/r/nvidia/cuda/tags)

#推荐在Dockefile-编译镜像不执行build.sh以最小化镜像, 在进入容器后手动执行sh /tmp/build.sh, 使用如下  
```
#预处理:
a.根据hub.docker.com找到需要的基础镜像名字，修改Dockefile第一行。
b.根据自己的挂载需要，修改docker-compose.yml的volumes和ports(宿主机:容器) -- 一般挂载一个代码文件和模型文件夹即可
#

. env.sh # 可选加入自定义镜像前缀, eg>. env.sh ywz111  #建议都加上一个前缀，否则默认使用当前文件夹名
# docker images 查看当前所有镜像
# build # 重新编译构造镜像，谨慎

#初次运行容器-见env.sh封装 
site #自动生成docker账号，自动绑定宿主机执行的用户，密码默认为123456，具有sudo等权限

#...配置自己的环境，如安装anaconda/pytorch/tensorflow等，如果可以写到build.sh，也可以手动装
sudo sh /tmp/build.sh #在此处进行环境搭建，最小化镜像
```
#如果后续可能有迁移需求，推荐使用[root安装conda并共享给docker说明](#rootconda)，以支持快速迁移
#注: 迁移后会自动将/home/docker进行chown递归刷改，其他文件如果有权限问题直接chmod -R 777即可。需要保存在镜像容器内的文件尽量放在其他位置加777权限再软链接到/home/docker/下，可减少迁移时fixuid时间

```
#注意:首次配置完成后，一定要运行以下命令
docker commit 容器名称(或容器ID) 生成的镜像名
#将配置好的容器环境提交并替换个人镜像，之后无论容器/宿主机重启，直接进入容器不需要重新配置环境
```

连接管理
```
#重新连接  
docker ps -a #查看所有容器
docker attach [CONTAINER_NAME or CONTAINER_ID] # 快速命令>attach [容器id前缀即可]
#热芝士:退出时，使用[ctrl + D]，这样会结束docker当前线程，容器结束，可以使用[ctrl + P][ctrl + Q]退出而不终止容器运行
or
#新开一个临时bash窗口到容器，结束时ctrl+D/ctrl+P+Q均可，里面需要进tmux跑程序
docker exec -it [CONTAINER_NAME or CONTAINER_ID] /bin/bash #快速命令>once [容器id前缀即可]
```

迁移docker
```
#如果替换可以不输[:标签]
docker commit -m="描述信息" -a="username" 容器名称|容器ID 生成的镜像名[:标签名]
docker save/export -o savePathName_xxx.tar 镜像名[:标签] 
docker load/import -i xxxx.tar
#如果觉得commit导致文件过大，可以采用export方式，只保留一层镜像
```

# 2.管理员配置完整过程[非管理员可忽略]  
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
1、如果普通用户执行docker命令，如果提示get …… dial unix /var/run/docker.sock权限不够，则修改/var/run/docker.sock权限
使用root用户执行如下命令，即可
```
sudo chmod a+rw /var/run/docker.sock #恢复则刷660
```

or  

```
#(不推荐此种方式，需要频繁重启docker)  
sudo groupadd docker   #需要先允许所有人执行docker命令  
sudo gpasswd -a [ywz/dyf/zyt] docker  # 把用户添加进docker组中  
sudo service docker restart  # 重启docker  
```

# 3.其他参考命令

## 管理员docker命令
```
#镜像清理
docker image prune
docker ps -a
docker ps -a -q
#停止/删除所有容器
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
#重入容器
docker attach xx # xx只需要输入id的部分前缀使其唯一即可, 例如7d16dasdaf => docker attach 7d
```

----

## <span id="rootconda">容器内部使用root配置conda共享给其他用户/conda迁移</span>
目的: 通过把conda装到root里再给docker用户使用，在容器迁移时进行fixuid时可自动跳过anaconda3文件夹，避免chown过大文件导致等待时间较长
```
#docker内执行！
sudo su #切换
cd /root/
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh #下载conda
sh ./Anaconda3-2021.11-Linux-x86_64.sh #进行安装
#安装过程省略，安装路径/usr/anaconda3/
#安装后记得选择yes

#处理权限
chmod -R 777 /usr/anaconda3/
echo 'export PATH="/usr/anaconda3/bin:$PATH"' >> /home/docker/.bashrc
su docker
cd /home/docker/
source ~/.bashrc #临时激活conda
conda init #激活自动启动
```
