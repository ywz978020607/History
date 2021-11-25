from machine import SPI,Pin
from ws2812 import *


spi = SPI(1)
spi.init(baudrate=3200000,mosi=Pin(23))

chain = WS2812(spi,led_count=1)
data=[
    (255,0,0) #red
]
chain.show(data)

