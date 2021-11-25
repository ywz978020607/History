from machine import Pin,SPI
import Screen
import time

power=Pin(13,Pin.OUT)
power.value(1)
spi=SPI(1,sck=Pin(18,Pin.OUT),mosi=Pin(5,Pin.OUT),baudrate=24000000)

# width:128, height:64, dc-->pin16, res-->pin17
s = Screen.create(128, 64, spi, Pin(22,Pin.OUT), Pin(23,Pin.OUT))
s.print('Hello, world.\nadbd')