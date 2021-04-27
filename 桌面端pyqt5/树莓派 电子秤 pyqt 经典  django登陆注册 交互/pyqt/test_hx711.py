#with installed hx711

import RPi.GPIO as GPIO
from hx711 import HX711
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()

hx.tare() #去皮
print(hx.get_weight(5)/92000)  #92 = 1g
