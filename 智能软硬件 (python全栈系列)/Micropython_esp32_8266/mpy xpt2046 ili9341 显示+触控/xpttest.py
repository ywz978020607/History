from machine import SPI
from xpt2046 import XPT2046
from time import sleep

spi = SPI(1, baudrate=1000000)

xpt = XPT2046(spi)

while True:
    p = xpt.get_touch(raw=True)
    if p is not None:
        print(p)
    sleep(0.1)
    if p[0] < 500 and p[1] < 500:
        break



