"""SSD1351 demo (images)."""
from time import sleep
from ssd1351 import Display
from machine import Pin, SPI


def test():
    """Test code."""
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(21))

    while 1:
        display.draw_image('1.raw',  0, 32, 128, 96)
        sleep(5)

        display.draw_image('2.raw',  0, 32, 128, 96)
        sleep(5)

    display.cleanup()


test()

"""
from time import sleep
from ssd1351 import Display
from machine import Pin, SPI


spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(21))

display.draw_image('11.raw', 0, 32+16, 20, 80) #32+0

display.clear()
"""