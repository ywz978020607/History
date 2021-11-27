#ws2812
from machine import *
from ws2812 import *

spi = SPI(1)
# spi.init(mosi=Pin(27))
spi.init(baudrate=3200000,mosi=Pin(27))


chain = WS2812(spi,led_count=16)
chain.set_color(0,(255,255,255))
chain.set_color(0,(255,0,0))
