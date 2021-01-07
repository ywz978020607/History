# ubuntu18 配置/etc/rc.local

https://blog.csdn.net/a912952381/article/details/81205095

1）将 /lib/systemd/system/rc-local.service 链接到 /etc/systemd/system/ 目录下面来：

ln -fs /lib/systemd/system/rc-local.service /etc/systemd/system/rc-local.service

sudo vim /etc/systemd/system/rc-local.service

在文件末尾添加

```
[Install]
WantedBy=multi-user.target
Alias=rc-local.service
```

sudo touch /etc/rc.local

chmod 755 /etc/rc.local

写rc.local文件即可 开头 #!/bin/bash



# usb重新连接

https://blog.csdn.net/weixin_43935474/article/details/102171095



cc usbreset.c -o usbreset

chmod +x usbreset

#lsusb  eg: -> Bus 002 Device 003: ID 0fe9:9010 DVICO 

sudo ./usbreset /dev/bus/usb/002/003 



# service一类的开机自启动

如nginx等服务类 [Linux服务器，服务管理--systemctl命令详解，设置开机自启动 - 大自然的流风 - 博客园 (cnblogs.com)](https://www.cnblogs.com/zdz8207/p/linux-systemctl.html)

```
sudo systemctl enable nginx
sudo systemctl enable supervisor
```