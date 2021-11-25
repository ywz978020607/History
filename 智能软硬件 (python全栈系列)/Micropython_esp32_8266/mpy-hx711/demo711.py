from machine import freq
freq(160000000)

from hx711 import HX711

driver = HX711(d_out=27, pd_sck=14)
driver
driver.read()

driver.channel=HX711.CHANNEL_A_64
driver.read()





