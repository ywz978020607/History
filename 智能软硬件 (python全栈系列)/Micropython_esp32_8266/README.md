# Micropython快速实现开源硬件开发

*开发硬件：esp32，刷入mpy固件*



- mywifi.py

  *连接wifi的类，利用多线程实现定时扫描，掉线重连，一行代码调用*

  ```python
  import mywifi
  m = mywifi.WIFI(SSID='yourwifiname',PASS='password',check=1) #check表示是否定时自检重连
  ```

  



欢迎大家加入，一同push