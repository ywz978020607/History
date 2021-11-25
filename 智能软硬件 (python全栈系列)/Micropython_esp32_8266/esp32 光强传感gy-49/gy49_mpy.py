import machine
from machine import I2C, Pin

import time

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

i2c.scan()
#74 0x4A(74)

# ##设置为连续读取模式 800ms一次
# buf = b'\x04\x00'
# i2c.writeto_mem(74, 0x02, buf)

#默认就是自动读
time.sleep(1)
##
data = i2c.readfrom_mem(74,  0x03, 2)
exponent = (data[0] & 0xF0) >> 4
mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
luminance = ((2 ** exponent) * mantissa) * 0.045
print(luminance)
