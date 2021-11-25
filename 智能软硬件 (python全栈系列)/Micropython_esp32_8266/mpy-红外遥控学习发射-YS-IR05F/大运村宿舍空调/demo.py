import dht
from machine import *

mydht = dht.DHT11(Pin(5))
mydht.measure()
temp = mydht.temperature()
print(temp)
