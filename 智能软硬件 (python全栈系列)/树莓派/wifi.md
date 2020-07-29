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