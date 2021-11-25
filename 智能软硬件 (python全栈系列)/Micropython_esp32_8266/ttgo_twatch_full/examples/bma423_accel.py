from machine import I2C
from machine import Pin
import bma423 as bma
import time

i2c = I2C(scl=22, sda=21,speed=400000)
bma.init(i2c)

while True:
	bma.accel()
	time.sleep_ms(200)