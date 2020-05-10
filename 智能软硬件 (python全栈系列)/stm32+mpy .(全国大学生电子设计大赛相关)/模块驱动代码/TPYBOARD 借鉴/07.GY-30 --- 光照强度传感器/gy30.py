import pyb
from pyb import Pin, I2C

class GY30:
	def __init__(self,id):
		self.accel_addr = 35
		self.i2c = pyb.I2C(id)
		self.i2c.init(pyb.I2C.MASTER, baudrate=400000)
		print(self.i2c.scan())

	def start(self):
		self.i2c.scan()
		self.i2c.is_ready(self.accel_addr)
		self.i2c.send(1,35)
		self.i2c.send(0x10,35)

	def read(self):
		self.i2c.scan()
		self.i2c.is_ready(self.accel_addr)
		self.data=self.i2c.mem_read(2, self.accel_addr, 0x47, timeout=1000,addr_size=8)
		return self.data