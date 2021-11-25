from test1 import *
from machine import Pin, SPI
import mfrc522

spi = SPI(miso=Pin(19), mosi=Pin(21, Pin.OUT), sck=Pin(22, Pin.OUT))
rst_pin = Pin(4,Pin.OUT)
sda_pin = Pin(23,Pin.OUT)
rfid = mfrc522.MFRC522(spi,rst_pin,sda_pin)

# rfid.read_card()
# get_name(rfid.read_card()[1])

data1 = set_name('1001')
data=data1+bytes(7)+set_value(20.0)

rfid.write_card(data)



