import dht
from machine import Pin

mydht = dht.DHT22(Pin(5))

mydht.measure()
temperature = mydht.temperature()

humidity = mydht.humidity()

print(temperature)
print(humidity)
