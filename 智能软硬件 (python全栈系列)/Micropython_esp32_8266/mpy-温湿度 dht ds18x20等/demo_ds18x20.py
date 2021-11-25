import machine
import time,onewire,ds18x20
from machine import Pin


ow=onewire.OneWire(Pin(5))#创建onewire总线 
ds=ds18x20.DS18X20(ow)
ds.scan()
roms = ds.scan()#扫描总线上的设备
ds.convert_temp()#获取采样温度
time.sleep_ms(750)

#获取最新温度  23.4375
temperature = ds.read_temp(roms[-1])
print(temperature)

# for rom in roms:
#     print(ds.read_temp(rom))#得到温度

