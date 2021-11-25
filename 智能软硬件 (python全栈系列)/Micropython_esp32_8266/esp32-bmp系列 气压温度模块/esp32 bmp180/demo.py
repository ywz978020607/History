from BMP180 import BMP180
from machine import Pin, I2C

bus = I2C(scl=Pin(4), sda=Pin(5), freq=100000)
bmp180 = BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

p = bmp180.pressure
altitude = round(-bmp180.altitude)




