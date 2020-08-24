from pyb import Pin
from ds18b20 import DS18X20

wd = DS18X20(Pin('Y10'))              #设置DS18B20 DO引脚为Y10

while True:
    print('当前温度:',wd.read_temp())
    pyb.delay(1000)