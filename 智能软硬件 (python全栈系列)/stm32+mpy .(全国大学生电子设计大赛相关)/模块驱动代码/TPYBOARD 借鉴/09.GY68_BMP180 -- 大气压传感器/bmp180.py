import pyb
import time
from pyb import I2C
  
BMP180_I2C_ADDR = 119
class BMP180():
	def __init__(self, i2c_num):
		self.i2c = I2C(i2c_num, I2C.MASTER, baudrate = 100000)
		self.i2c.scan()
		self.i2c.is_ready(BMP180_I2C_ADDR)
		self.AC1 = self.short(self.getReg(0xAA))
		self.AC2 = self.short(self.getReg(0xAC))
		self.AC3 = self.short(self.getReg(0xAE))
		self.AC4 = self.getReg(0xB0)
		self.AC5 = self.getReg(0xB2)
		self.AC6 = self.getReg(0xB4)
		self.B1 = self.short(self.getReg(0xB6))
		self.B2 = self.short(self.getReg(0xB8))
		self.MB = self.short(self.getReg(0xBA))
		self.MC = self.short(self.getReg(0xBC))
		self.MD = self.short(self.getReg(0xBE))
		self.UT = 0
		self.UP = 0
		self.B3 = 0
		self.B4 = 0
		self.B5 = 0
		self.B6 = 0
		self.B7 = 0
		self.X1 = 0
		self.X2 = 0
		self.X3 = 0
		
	def	readpress(self):
		self.i2c.is_ready(BMP180_I2C_ADDR)
		self.setReg(0x34,0xf4)
		time.sleep_ms(5)

		self.i2c.send(bytearray(0xf6), BMP180_I2C_ADDR)
		up=list(self.i2c.mem_read(2, BMP180_I2C_ADDR, 0xf6, timeout=1000,addr_size=8))
		up=up[0]<<8|up[1]
		
		b6 = self.b5 - 4000
		x1 = (self.B2*((b6*b6)/(1<<12)))/(1<<11)
		x2 = (self.AC2*b6)/(1<<11)
		x3 = (x1+x2)
		b3 = ((self.AC1*4+x3)+2)/4
		x1 = (self.AC3*b6)/(1<<13)
		x2 = (self.B1*((b6*b6)/(1<<12)))/(1<<16)
		x3 = (x1+x2+2)/(1<<2)
		b4 = (self.AC4*(x3+32768))/(1<<15)
		b7 = (up-b3)*50000
		if b7 < 0x80000000:
			p = (b7*2)/b4
		else:
			p = (b7/b4)*2
		x1 = (p/(1<<8))*(p/(1<<8))
		x1 = (x1*3038)/(1<<16)
		x2 = (-7357*p)/(1<<16)
		self.p = p + ((x1 + x2 + 3791)/(1<<4))
		
		return self.p
		
	def	readtemp(self):
		self.i2c.is_ready(BMP180_I2C_ADDR)
		self.setReg(0x2e,0xf4)
		time.sleep_ms(5)

		ut=list(self.i2c.mem_read(2, BMP180_I2C_ADDR, 0xf6, timeout=1000,addr_size=8))
		ut=ut[0]<<8|ut[1]
		x1=(ut-self.AC6)*self.AC5>>15
		x2=(self.MC<<11)/(x1+self.MD)
		self.b5=x1+x2
		return round((self.b5+8)/10/16,2)
		
	def	readaltitude(self):
		return round((44330.0*(1.0-pow((float)(self.p)/101325.0,1.0/5.255))),2)
  
	def short(self, dat):
		if dat > 32767:
			return dat - 65536
		else:
			return dat
	 
	def setReg(self, dat, reg):
		buf = bytearray(2)
		buf[0] = reg
		buf[1] = dat
		self.i2c.send(buf, BMP180_I2C_ADDR)
		 
	def getReg(self, reg):
		t=list(self.i2c.mem_read(2, BMP180_I2C_ADDR, reg, timeout=1000,addr_size=8))
		t=t[0]<<8|t[1]
		return t