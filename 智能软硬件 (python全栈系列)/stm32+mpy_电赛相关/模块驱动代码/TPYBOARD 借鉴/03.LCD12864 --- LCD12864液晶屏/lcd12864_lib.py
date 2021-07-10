#地址	80-87
#		90-97
#		88-8F
#		98-9F
import pyb
import time

class LCD12864:

	def __init__(self,rs,e):
		self.rs=pyb.Pin(rs,pyb.Pin.OUT_PP)
		self.e=pyb.Pin(e,pyb.Pin.OUT_PP)
		self.lcd_write(0x30,0)
		pyb.delay(50)
		self.lcd_write(0x06,0)
		pyb.delay(50)
		self.lcd_write(0x01,0)
		pyb.delay(50)
		self.lcd_write(0x0c,0)
		pyb.delay(50)
		self.lcd_write(0x02,0)
		pyb.delay(50)
		self.qp_12864()
		
	def qp_12864(self):
		self.lcd_write(0x3f,0)
		self.lcd_write(0xc0,0)
		pyb.delay(5)
		self.lcd_write(0x34,0)
		self.lcd_write(0x36,0)
		pyb.delay(5)

		for i in range(32):
			self.lcd_write(0x80+i,0)
			self.lcd_write(0x80,0)
			for j in range(32):
				self.lcd_write(0x0,1)
		self.lcd_write(0x30,0)
		self.lcd_write(0xc0,0)
		pyb.delay(5)
				
	def lcd_write(self,addr,ms):
		self.e.value(0)
		self.rs.value(ms)
		c="X1"
		d=list(c)
		for i in range(8):
			b=addr&1
			addr>>=1
			pyb.Pin(''.join(d),pyb.Pin.OUT_PP).value(b)
			d[1]=str(int(d[1])+1)
		pyb.delay(1)
		self.e.value(1)
		pyb.delay(1)
		self.e.value(0)
				
	def lcd_write_string(self,address,string,s_bit):
		self.lcd_write(address,0)
		a=(len(string)-(s_bit-1))*s_bit
		for j in range(a):
			self.lcd_write(bytearray(string)[j],1)