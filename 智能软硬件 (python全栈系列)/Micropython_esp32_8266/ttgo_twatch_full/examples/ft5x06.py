import machine
import touchscreen as ts
import time

sda_pin = machine.Pin(23)
scl_pin = machine.Pin(32)

i2c = machine.I2C(scl=scl_pin, sda=sda_pin, speed=400000)

ts.init(i2c)

while True:
  ts.read()
  time.sleep(0.2);
