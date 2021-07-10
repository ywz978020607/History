# MicroPython ST7735 TFT display HAL

import time
from pyb import SPI,Pin
import os, gc
from struct import unpack

LCD_W=129
LCD_H=163

WHITE	=		0xFFFF
BLACK	=		0x0000	  
BLUE	=		0x001F	 
BRED	=		0XF81F
GRED	=	 	0XFFE0
GBLUE	=	 	0X07FF
RED		=		0xF800
MAGENTA	=		0xF81F
GREEN	=		0x07E0
CYAN	=		0x7FFF
YELLOW	=		0xFFE0
BROWN	=		0XBC40 #//棕色
BRRED	=		0XFC07 #//棕红色
GRAY	=		0X8430 #//灰色

class TFT:
	def __init__(self,spi,cs,rst,rs,color):
		spi.init(spi.MASTER,baudrate=1000000,polarity=0, phase=0,bits=8,firstbit=SPI.MSB)
		self.spi=spi
		self.color=color
		self.rst=Pin(rst,Pin.OUT_PP)
		self.cs=Pin(cs,Pin.OUT_PP)
		self.rs=Pin(rs,Pin.OUT_PP)
		self.Init()
		
	def Init(self):
		self.cs.value(1)
		self.rst.value(1)
		time.sleep_ms(5)
		self.rst.value(0)
		time.sleep_ms(5)
		self.rst.value(1)
		self.cs.value(1)
		time.sleep_ms(5)
		self.cs.value(0)
		self.writecmd(0x11)
		time.sleep_ms(120)
		
		self.writecmd(0xb1)
		self.writedata(0x05)
		self.writedata(0x3c)
		self.writedata(0x3c)
		self.writecmd(0xb2)
		self.writedata(0x05)
		self.writedata(0x3c)
		self.writedata(0x3c)
		self.writecmd(0xb3)
		self.writedata(0x05)
		self.writedata(0x3c)
		self.writedata(0x3c)
		self.writedata(0x05)
		self.writedata(0x3c)
		self.writedata(0x3c)
		
		self.writecmd(0xb4)
		self.writedata(0x03)
		self.writecmd(0xc0)
		self.writedata(0x28)
		self.writedata(0x08)
		self.writedata(0x04)
		self.writecmd(0xc1)
		self.writedata(0xc0)
		self.writecmd(0xc2)
		self.writedata(0x0d)
		self.writedata(0x00)
		self.writecmd(0xc3)
		self.writedata(0x8d)
		self.writedata(0x2a)
		self.writecmd(0xc4)
		self.writedata(0x8d)
		self.writedata(0xee)
		
		self.writecmd(0xc5)
		self.writedata(0x1a)
		self.writecmd(0x36)
		self.writedata(0xc0)
		
		self.writecmd(0xe0)
		self.writedata(0x04)
		self.writedata(0x22)
		self.writedata(0x07)
		self.writedata(0x0a)
		self.writedata(0x2e)
		self.writedata(0x30)
		self.writedata(0x25)
		self.writedata(0x2a)
		self.writedata(0x28)
		self.writedata(0x26)
		self.writedata(0x2e)
		self.writedata(0x3a)
		self.writedata(0x00)
		self.writedata(0x01)
		self.writedata(0x03)
		self.writedata(0x13)
		
		self.writecmd(0xe1)
		self.writedata(0x04)
		self.writedata(0x16)
		self.writedata(0x06)
		self.writedata(0x0d)
		self.writedata(0x2d)
		self.writedata(0x26)
		self.writedata(0x23)
		self.writedata(0x27)
		self.writedata(0x27)
		self.writedata(0x25)
		self.writedata(0x2d)
		self.writedata(0x3b)
		self.writedata(0x00)
		self.writedata(0x01)
		self.writedata(0x04)
		self.writedata(0x13)
		
		self.writecmd(0x3a)
		self.writedata(0x05)
		self.writecmd(0x29)
		
	def	clean(self,color):
		VH=color>>8
		VL=color
		self.address_set(0,0,LCD_W,LCD_H)
		for i in range(LCD_W):
			for k in range(LCD_H):
				self.writedata(VH)
				self.writedata(VL)
				
	def	writecmd(self,cmd):
		self.rs.value(0)
		self.spi.send(cmd)
		
	def	writedata(self,data):
		self.rs.value(1)
		self.spi.send(data)
		
	def	address_set(self,x,y,w,h):
		self.writecmd(0x2a)
		self.writedata(x>>8)
		self.writedata(x)
		self.writedata(w>>8)
		self.writedata(w)
		
		self.writecmd(0x2b)
		self.writedata(y>>8)
		self.writedata(y)
		self.writedata(h>>8)
		self.writedata(h)
		
		self.writecmd(0x2c)
		
	def	writecolor(self,color):
		self.rs.value(1)
		self.spi.send(color>>8)
		self.spi.send(color)
		
	def	point(self,x,y,color):
		self.address_set(x,y,x,y)
		self.writecolor(color)
		
	def	line(self,xs,ys,xe,ye,color):
		x=xe-xs
		y=ye-ys
		sx=xs
		sy=ys
		xerr=0
		yerr=0
		if(x>0):
			incx=1
		elif x==0:
			incx=0
		else :
			incx=-1
			x=-x
		if(y>0):
			incy=1
		elif y==0:
			incy=0
		else :
			incy=-1
			y=-y
		if x>y:
			xy=x
		else :
			xy=y
		for i in range(xy+1):
			self.point(sx,sy,color)
			xerr+=x
			yerr+=y
			if (xerr>xy):
				xerr-=xy
				sx+=incx
			if (yerr>xy):
				yerr-=xy
				sy+=incy
				
	def	fill(self,xs,ys,xe,ye,color):
		self.address_set(xs,ys,xe,ye)
		for i in range(xe-xs):
			for k in range(ye-ys):
				self.writecolor(color)
				
	def	rectangle(self,x1,y1,x2,y2,color):
		self.line(x1,y1,x2,y1,color)
		self.line(x1,y1,x1,y2,color)
		self.line(x1,y2,x2,y2,color)
		self.line(x2,y1,x2,y2,color)
	
	def	round(self,x0,y0,r,color):
		a=0
		b=r
		di=3-(r<<1)
		while (a<=b):
			self.point(x0-b,y0-a,color)
			self.point(x0+b,y0-a,color)
			self.point(x0-a,y0+b,color)
			self.point(x0-b,y0-a,color)
			self.point(x0-a,y0-b,color)
			self.point(x0+b,y0+a,color)
			self.point(x0+a,y0-b,color)
			self.point(x0+a,y0+b,color)
			self.point(x0-b,y0+a,color)
			a+=1
			if (di<0):
				di+=4*a+6
			else :
				di+=10+4*(a-b)
				b-=1
			self.point(x0+a,y0+b,color)
			
	def	data8(self,data,color):
		for i in range(8):
			a=(data&0x80)>>7
			if (a):
				self.writecolor(color)
			else :
				self.writecolor(self.color)
			data<<=1
			
	def	write(self,x,y,a,b,fist,color):
		self.address_set(x,y,a-1,b-1)
		for i in range(int((a-x)*(b-y)/8)):
			self.data8(self.font[i+fist],color)
	
	def	write_str(self,x,y,wight,high,string,color):
		# wight=int((a-x)/len(string))
		a=x+wight
		b=y+high
		for i in range(len(string)):
			fist=self.indexes.index(string[i])*int(wight*high/8)
			self.write(x,y,a,b,fist,color)
			x+=wight
			a+=wight
			
	def	write_img(self,x,y,img):
		self.address_set(x,y,(x+(img[2]<<8)+img[3])-1,(y+(img[4]<<8)+img[5])-1)
		i=8
		while i<(2*((img[2]<<8)+img[3])*((img[4]<<8)+img[5])):
			self.writecolor((img[i]<<8)|(img[i+1]))
			i+=2
	
	def	write_pictuer(self,x,y,wight,high,pictuer,color):
		self.address_set(x,y,x+wight-1,y+high-1)
		for i in range(len(pictuer)):
			self.data8(pictuer[i],color)

			
	def	init_str(self,font,indexes):
		self.font=font
		self.indexes=indexes
		
	def displayfile(self, name, x,y,width, height):
		with open(name, "rb") as f:
			gc.collect()
			row = 0
			parts = name.split(".") # get extension
			if len(parts) > 1:
				mode = parts[-1].lower()
			if mode == "bmp":	 # Windows bmp file
				BM, filesize, res0, offset = unpack("<hiii", f.read(14))
				(hdrsize, imgwidth, imgheight, planes, colors, compress, imgsize, 
				 h_res, v_res, ct_size, cti_size) = unpack("<iiihhiiiiii", f.read(40))
				if imgwidth <= width: ##
					skip = ((height - imgheight) // 2)
					if skip > 0:
						self.fillRectangle(0, height - skip, width - 1, height - 1, (0, 0, 0))
					else:
						skip = 0
					if colors in (1,4,8):  # must have a color table
						if ct_size == 0: # if 0, size is 2**colors
							ct_size = 1 << colors
						colortable = bytearray(ct_size * 4)
						f.seek(hdrsize + 14) # go to colortable
						n = f.readinto(colortable) # read colortable
						if colors == 1:
							bsize = imgwidth // 8
						elif colors == 2:
							bsize = imgwidth // 4
						elif colors == 4:
							bsize = imgwidth // 2
						elif colors == 8:
							bsize = imgwidth
						bsize = (bsize + 3) & 0xfffc # must read a multiple of 4 bytes
						b = bytearray(bsize)
						f.seek(offset)
						for row in range(height - skip - 1, -1, -1):
							n = f.readinto(b)
							if n != bsize:
								break
							self.address_set(x,row+y,x+width-1,row+y)
							# print(0,row,width,row)
							for i in range(0,width-1,+1):
								self.rs.value(1)
								# self.spi.send(b[i+2])
								self.spi.send(b[i+0])
								self.spi.send(b[i+0])
					else:
						f.seek(offset)
						if colors == 16:
							bsize = (imgwidth*2 + 3) & 0xfffc # must read a multiple of 4 bytes
							b = bytearray(bsize)
							for row in range(height, -1, -1):
								n = f.readinto(b)
								if n != bsize:
									break
								self.address_set(x,row+y,x+width-1,row+y)
								# print(0,row,width,row)
								for i in range(0,width*2-1,+2):
									self.rs.value(1)
									self.spi.send(b[i+2])
									self.spi.send(b[i+1])
									# self.spi.send(b[i+0])
								
						elif colors == 24:
							bsize = (imgwidth*3 + 3) & 0xfffc # must read a multiple of 4 bytes
							b = bytearray(bsize)
							for row in range(height - skip - 1, -1, -1):
								n = f.readinto(b)
								if n != bsize:
									break
								self.drawBitmap(0, row, imgwidth, 1, b, colors)
		f.close()