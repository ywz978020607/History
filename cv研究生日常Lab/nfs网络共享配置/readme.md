# 网络共享配置
## 注意: IRC实验室以硬盘为单位进行共享，非管理员不要直接操作以下内容，如有需要直接联系管理员


使用nfs，局域网只保留一份数据，各机器采用docker进行部署。

1 server <-> multi clients

https://cloud.tencent.com/developer/article/1626660


## server
```
sudo apt install nfs-kernel-server  

sudo vim /etc/exports
//在文件末尾添加一行
# /path-to-share                *(rw,sync)     //path-to-share是要共享的目录，根据自己情况修改
/temp_disk2                *(rw,sync)
#之后重启即可

sudo service nfs-kernel-server restart

sudo exportfs -v #查看
```

## client
```
sudo apt install nfs-common

showmount -e 10.134.126.158 #查看

sudo mkdir -p /srv/s930
sudo mount -t nfs -o vers=4 10.134.126.158:/home2 /srv/s930
#同步修改持久化挂载, 重启自动生效
sudo vim /etc/fstab
#add
10.134.126.158:/home2 /srv/s930       nfs   defaults 0 0
#
#不重启生效:
#sudo mount -a

df -h
```


