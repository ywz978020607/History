1）扫描周围的网络

sudo iwlist wlan0 scan

命令会列出所有可使用的wifi网络，以及网络的一些有用信息。例如：

1、ESSID:"testing" ：wifi网络的名字。

2、IE:IEEE 802.11i/WPA2 Version1 ：网络的验证方式，在这里是WPA2，本指南应该适用于WEP、WPA或者WPA2，但是可能不适用企业版WPA2；同样需要知道wifi网络的密码，本例WiFi密码：testingPassword

2）添加网络到树莓派

使用nano编辑器打开wpa-supplicant配置文件：

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

在文件的底部添加下面内容，编辑完按ctrl+x键然后按y键，最后再按回车键：

network={

  ssid="The_ESSID_from_Scan"

  psk="Your_wifi_password"

}

 

在本示例中，应该添加为：

network={

  ssid="testing"

  psk="testingPassword"

}

3）重启树莓派网络配置

sudo iwconfig wlan0 txpower off #关闭WiFi网络

sudo iwconfig wlan0 txpower on #打开WiFi网络

或者直接使用sudo reboot命令重启树莓派

4）验证是否成功连接网络

ifconfig wlan0  #确认是否已经成功连接上网络。如果inet addr中已经有地址了，说明树莓派成功连接上了网络。如果没有，请检查你的密码和ESSID是否正确。

-----------------

首次使用不用显示屏

 windows看到的TF卡变成了空间很小的名为boot的盘，我们在此目录下新建一个名为`wpa_supplicant.conf`空白文件 

```
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="WiFi名字，不删除引号,不能有中文"
	psk="WiFi密码，不删除引号"
	priority=将我替换成数字，数字越大代表优先级越高
}
```



----------------------

创建热点

 1.git clone [https://github.com/oblique/create_ap.git](http://jump.bdimg.com/safecheck/index?url=rN3wPs8te/r8jfr8YhogjfUWFoMgIRa8gmEfnfh3bF7/5yMFkkUiUowA0wIei9q7vZuLXXQ5XbpibHRw/0CV3/G+ZXSNVg8H/NVbSGovfJqXNbENAVozRW92wnbyB7iOGn4202Kl3jhNgHUaKJ1uuFX3ZMCahZXTMDxm7iZ2BjQ=)
2.cd create_ap
3.sudo make install就这样安装好了
4.接下来安装依赖库sudo apt-get install util-linux procps hostapd iproute2 iw haveged dnsmasq
5.就这么简单几个命令就能安装好全部环境
6.接下来保证你的网线插在pi3上并且能上网就行了。输入下面的命令启动无线AP：
sudo create_ap wlan0 eth0 热点名 密码 

