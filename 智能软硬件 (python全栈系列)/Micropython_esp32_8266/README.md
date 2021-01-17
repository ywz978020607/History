# Micropython快速实现开源硬件开发

*开发硬件：esp32，刷入mpy固件*



- mywifi.py

  *连接wifi的类，利用多线程实现定时扫描，掉线重连，一行代码调用*

  ```python
  import mywifi
  m = mywifi.WIFI(SSID='yourwifiname',PASS='password',check=1) #check表示是否定时自检重连
  ```

  



欢迎大家加入，一同push





特殊点记录：

- esp32

1. esp32的GPIO12与众不同，如果接上拉电阻，开机时导致flash电平设置为1.8V，无法正常开机，所以需要对其进行解离，操作见esp32-SDIO文件夹内，通过esptool工具进行熔断操作，然后可以放心使用GPIO12.

2. 蓝牙与wifi共用天线，尽量不要同时开启

3. wifi开启时，ADC2用不了，只能用ADC1的资源，对应引脚为32-39，与8266不同：

   除此之外，输入电压范围也有要求：

   - `ADC.ATTN_0DB`: 0dB attenuation, gives a maximum input voltage of 1.00v - this is the default configuration
   - `ADC.ATTN_2_5DB`: 2.5dB attenuation, gives a maximum input voltage of approximately 1.34v
   - `ADC.ATTN_6DB`: 6dB attenuation, gives a maximum input voltage of approximately 2.00v
   - `ADC.ATTN_11DB`: 11dB attenuation, gives a maximum input voltage of approximately 3.6v
   - 3.6V不能长时间，否则容易烧坏IC.

4. 硬件spi：

   ```
   hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
   vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
   ```

5. 扩展SD有两种方式：SDIO或SPI，而8266只有SPI方式。





- esp8266

  1. 与esp32不同，8266的deep-sleep需要GPIO16短接rst。而8266-01没有引出，用不了；8266-12可以有。

  2. ADC比较特殊，只有一个且范围最高1.0V

     ESP8266只有一个专用的ADC输入端口

     ```
     import machine
     adc = machine.ADC(0)        # create an ADC object
     val = adc.read()          # read an analog value
     ```
  
  3. 8266-01的UDP只能监听、不能发送！！




## 再推荐一个micropython的库集合

https://github.com/mcauser/awesome-micropython

