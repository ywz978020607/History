from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont

spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(21))
espresso_dolce = XglcdFont('EspressoDolce18x24.c', 18, 24)
# unispace = XglcdFont('Unispace12x24.c', 12, 24)

display.clear()
# 对联
# display.draw_image('00.raw', 0, 32+0, 128, 96) #32+0
#左 踏雪马蹄香 20x80
display.draw_image('11.raw', 0, 32+16, 20, 80) #32+0
#右 20x80
display.draw_image('22.raw', 107, 32+16, 20, 80) #32+0
#横 72x18
display.draw_image('33.raw', -36+128//2, 32+0, 72, 18) #32+0

# 时间
#     display.draw_text(0, 36, 'Espresso', espresso_dolce,
#                       color565(0, 255, 255))
display.draw_text(40,32+25,'10',espresso_dolce,color565(0,255,255))
display.draw_text(65,32+25,':',espresso_dolce,color565(255,0,255))
display.draw_text(73,32+25,'00',espresso_dolce,color565(255,255,0))

# 天气 38x36
display.draw_image('sun.raw', -36+128//2, 32+55, 38,36) #32+0
display.draw_text(-36+128//2+45,32+48,'-6',espresso_dolce,color565(255,0,255))
display.draw_text(-36+128//2+45,32+72,'+10',espresso_dolce,color565(255,0,255))

