import pyb
from pyb import Pin, I2C
from gy30 import GY30
	
gy30=GY30(1)
gy30.start()
while True:
	a=gy30.read()
	print(a[0]*0xff+a[1])