import time
from am2320 import AM2320
am_2320 = AM2320.AM2320(1)

while True:
	am_2320.measure()
	print('温度:',am_2320.temperature())
	print('湿度:',am_2320.humidity())
	time.sleep_ms(500)