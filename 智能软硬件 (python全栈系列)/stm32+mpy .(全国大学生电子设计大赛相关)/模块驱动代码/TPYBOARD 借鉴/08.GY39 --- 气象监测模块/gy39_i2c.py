import pyb
from pyb import I2C

class GY39I2C:
	def __init__(self,i2c):
		self.i2c = pyb.I2C(i2c)
		self.i2c.init(pyb.I2C.MASTER, addr=43,baudrate=40000,gencall = True,dma = False)
		self.addr=self.i2c.scan()[0]

	def	read(self):
		self.i2c.is_ready(self.addr)
		i=0
		while 1:
			try:
				hc=self.i2c.mem_read(14,i,0,timeout=500,addr_size=8)
				l=(hc[0]<<24)|(hc[1]<<16)|(hc[2]<<8)|hc[3]
				t=((hc[4]<<8)|hc[5])/100
				p=((hc[6]<<24)|(hc[7]<<16)|(hc[8]<<8)|hc[9])/100
				h=((hc[10]<<8)|hc[11])/100
				H=((hc[12]<<8)|hc[13])
				return l,t,p,h,H
			except OSError:
				i+=1