
#py-base 01studio
import ili9341
from machine import Pin, SPI

from xpt2046 import XPT2046
from time import sleep

#6个引脚
spi = SPI(miso=Pin(12), mosi=Pin(13, Pin.OUT), sck=Pin(14, Pin.OUT))  #240*320 
#or add : scroll = True ->scroll 320*240
display = ili9341.ILI9341(spi, cs=Pin(15), dc=Pin(21), rst=Pin(33))
display.fill(ili9341.color565(0xff, 0x11, 0x22))
display.pixel(120, 160, 0)
##########################

#触摸 +2个引脚
#Y1-PEN-0
#Y2-CS2-2
pen = Pin(0,Pin.OUT)
pen.off()
cs2 = Pin(2,Pin.OUT)
cs2.off()

# spi = SPI(1, baudrate=1000000)
xpt = XPT2046(spi)

while True:
    p = xpt.get_touch(raw=True)
    if p is not None:
        print(p)
    sleep(0.1)
    if p[0] < 500 and p[1] < 500:
        break


##更简单的方法，直接通过Pen：1-》0 判断按下，然后读取 xpt.raw_touch() -> (2143,2399)

