# 网络共享配置

使用nfs，局域网只保留一份数据，各机器采用docker进行部署。

https://cloud.tencent.com/developer/article/1626660

可将下面www换成个人名字，再进行配置

## server
```
sudo apt install nfs-kernel-server  
sudo mkdir -p /srv/nfs4/www

#sudo mount --bind /var/www /srv/nfs4/www
#持久化挂载
sudo vim /etc/fstab
#add
/var/www     /srv/nfs4/www      none   bind   0   0
#

#导出文件系统时, 允许所有ip访问
sudo vim /etc/exports
#add
/srv/nfs4         *(rw,sync,no_subtree_check,crossmnt,fsid=0)
#

sudo exportfs -ra #保存文件并导出分享
sudo exportfs -v #查看
```

## client
```
sudo apt install nfs-common
sudo mkdir -p /srv/www

#sudo mount -t nfs -o vers=4 192.168.33.xx:/www /srv/www
#持久化挂载
sudo vim /etc/fstab
#add
192.168.33.10:/www /srv/www       nfs   defaults,timeo=900,retrans=5,_netdev	0 0
#

df -h
```


