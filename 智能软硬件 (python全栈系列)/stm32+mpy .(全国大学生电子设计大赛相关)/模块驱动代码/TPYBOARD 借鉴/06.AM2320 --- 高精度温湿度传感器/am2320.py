"""
MicroPython Aosong AM2320 I2C driver
"""

import ustruct
import time
from pyb import Pin, I2C
import pyb
class AM2320:
	def __init__(self, id=1, address=0x5c):
		self.i2c = pyb.I2C(id)
		self.i2c.init(pyb.I2C.MASTER, baudrate=400000)
		self.address = address
		self.buf = bytearray(8)

	def measure(self):
		buf = self.buf
		address = self.address
		self.i2c.scan()
		if(self.i2c.is_ready(self.address)!=True):
			print('not found AM2320')
		try:
			self.i2c.send(b'',address)
		except AttributeError:
			pass
		self.i2c.send(b'\x03\x00\x04',address)
		time.sleep_ms(2)
		self.i2c.recv(buf, address, timeout=5000)
		crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]
		if (crc != self.crc16(buf[:-2])):
			raise Exception("checksum error")

	def crc16(self, buf):
		crc = 0xFFFF
		for c in buf:
			crc ^= c
			for i in range(8):
				if crc & 0x01:
					crc >>= 1
					crc ^= 0xA001
				else:
					crc >>= 1
		return crc

	def humidity(self):
		return (self.buf[2] << 8 | self.buf[3]) * 0.1

	def temperature(self):
		t = ((self.buf[4] & 0x7f) << 8 | self.buf[5]) * 0.1
		if self.buf[4] & 0x80:
			t = -t
		return t