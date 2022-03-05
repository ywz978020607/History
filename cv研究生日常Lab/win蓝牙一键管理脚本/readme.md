# 使用命令行管理蓝牙设备断开/链接

1. 安装工具 http://bluetoothinstaller.com/bluetooth-command-line-tools/  
2. 使用安装好的command line tools进入后查看对应设备的地址btdiscovery
```
btdiscovery

#输出
(30:21:69:15:26:74)     <Unknown name>  Hands Free
(7C:9A:1D:B8:61:C8)     ywzAirpods2     Headphones
(38:18:4C:12:5C:B3)     WH-1000XM3      Headset
(9C:19:C2:33:B5:06)     <Unknown name>  Unknown
(74:4C:A1:D8:C1:56)     LAPTOP-FL709PQ1 Laptop
(14:5A:FC:15:D6:F8)     LAPTOP-RBR9PDGG Laptop
(7C:A1:77:DF:F9:9A)     Metro   Smartphone
```  
3. 连接/断开
```
#断开-r  HFP语音是111e  A2DP音乐110b
btcom.exe -n "WH-1000XM3" -r -s111e
btcom.exe -n "WH-1000XM3" -r -s110b

#连接-c  HFP语音是111e  A2DP音乐110b
btcom.exe -n "WH-1000XM3" -c -s111e
btcom.exe -n "WH-1000XM3" -c -s110b
```

4. 将[-n 名称]换成[-b 地址]会显著提速
```
#断
btcom.exe -b "38:18:4C:12:5C:B3" -r -s111e
btcom.exe -b "38:18:4C:12:5C:B3" -r -s110b

#连
btcom.exe -b "38:18:4C:12:5C:B3" -c -s111e
btcom.exe -b "38:18:4C:12:5C:B3" -c -s110b
```

5. btdiscovery查看连接状态
```
btdiscovery.exe -b 38:18:4C:12:5C:B3 -d "%c%"
#输出
Yes
No
```