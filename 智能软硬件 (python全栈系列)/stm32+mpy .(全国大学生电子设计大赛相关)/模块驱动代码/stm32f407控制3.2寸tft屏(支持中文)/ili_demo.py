import myb.ili9341 as ili9341
from myb.colors import *
from machine import Pin, SPI
spi = SPI(miso=Pin(12), mosi=Pin(13, Pin.OUT), sck=Pin(14, Pin.OUT))
lcd = ili9341.ILI9341(spi, cs=Pin(33), dc=Pin(5), rst=Pin(4),scroll=True)  #True<=>Landscape,False<=>Portrait
#size is lcd.width * lcd.height

lcd.fill(ili9341.color(RED))

lcd.fill(0xffff)
lcd.text("2019",40,40)


lcd.chstrH(100,100,['全','国','电','设'],num=4)
lcd.chstrV(100,130,['快','乐','暑','假'],num=4)


lcd.fill(ili9341.color565(0xff, 0xff, 0xff))

lcd.pixel(20,20,ili9341.color565(0xff, 0x11, 0x22))

