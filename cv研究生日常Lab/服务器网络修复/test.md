# 查看网卡

### **dmesg | grep -i eth** 













# wifi

方法一：iwconfig

iwlist wlan0 scan  # 记下essid

iwconfig wlan0 essid ChinaNet  #其中ChinaNet是搜索到的无线网essid

iwconfig wlan0 essid ChinaNet key xxxx  #其中xxxx是密码

ifconfig wlan0 up #启动网卡

dhclient wlan0　或 dhcpcd wlan0  #通过dhcp获取IP　



方法二：wpa_cli

操作步骤：

shell 中输入 wpa_cli 进入交互，然后输入

> add_network
>
> \# 执行后会返回一个数字（一般是0），下面会用到，暂且称为 NID
>
> set_network NID ssid “WIFI SSID，根据你的网络环境填写”
>
> set_network NID psk “无线密码”
>
> bssid NID "BSSID", 设置bssid。
>
> enable_network NID
>
> \# 启用网络，成功后会返回 CONNECT TO XXXX的
>
> 然后就可以输入q退出了

退出后使用 dhclient wlan0 获取一下网络地址就可以使用了

