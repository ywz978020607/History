## 📽 基于Esp32-Cam 的 IP-Camera
版本1.0.0

## 📍 特性
1. 支持多客户端
2. 支持stream流
3. 支持snapshot
4. 支持在线浏览
5. 支持设置密钥获取

## 📜未来计划
1. 增加OTA更新
2. more

## 📌用法

### 配置环境
```
pip3 install esptool
pip3 install adafruit-ampy
```

### 刷入固件
#### 假如为COM12,先擦除ESP32-CAM
```
python3 -m esptool.py --chip esp32 --port COM12  erase_flash
```

#### 刷入固件
固件在bin目录下
```
cd bin
python3 -m esptool.py --chip esp32 --port COM12  write_flash -z 0x1000 esp32cam-mirco_python_v1.11-665-gfb0141559-kaki5.bin
```

#### 配置config.json
将里面的wifi_ssid和wifi_password与自己的WiFi名和密码对应
若有安全需要,则修改apikey就行

### 上传文件
```
ampy --port COM12 put main.py
ampy --port COM12 put config.json
ampy --port COM12 put boot.py
ampy --port COM12 put uasyncio
ampy --port COM12 put WIFI
```
### 运行
上传成功后,按下reset键,已知config.json中的apikey为esp32Camera</br>
在浏览器打开(实时观看):```http://esp32-cam的IP/webcam/esp32Camera```</br>
(获取视频流):```http://esp32-cam的IP/stream/esp32Camera```</br>
(获取照片):```http://esp32-cam的IP/snapshot/esp32Camera```