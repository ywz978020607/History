# ubuntu18 配置/etc/rc.local

https://blog.csdn.net/a912952381/article/details/81205095



记得 755 权限赋值





# usb重新连接

https://blog.csdn.net/weixin_43935474/article/details/102171095



cc usbreset.c -o usbreset

chmod +x usbreset

#lsusb  eg: -> Bus 002 Device 003: ID 0fe9:9010 DVICO 

sudo ./usbreset /dev/bus/usb/002/003 