import pyb
from pyb import SPI,Pin
import time

WC =0X00
RC =0X10
WTP=0X20
RTP=0X21
WTA=0X22
RTA=0X23
PRP=0X24

class NRF905:
	def __init__(self,spi,ce,txen,pwr,cd,dr,cs,RFConf,TxAddress):
		spi.init(spi.MASTER,baudrate=1000000,polarity=0, phase=0,bits=8,firstbit=SPI.MSB)
		self.spi=spi
		self.ce=Pin(ce,Pin.OUT_PP)
		self.txen=Pin(txen,Pin.OUT_PP)
		self.pwr=Pin(pwr,Pin.OUT_PP)
		self.cs=Pin(cs,Pin.OUT_PP)
		self.cd=Pin(cd,Pin.IN)
		self.dr=Pin(dr,Pin.IN)
		self.RFConf=RFConf
		self.TxAddress=TxAddress
		
		self.cs.value(1)
		self.dr.value(0)
		self.cd.value(0)
		self.pwr.value(1)
		self.ce.value(0)
		self.txen.value(0)
		self.Config905()
		
	def	Config905(self):
		self.cs.value(0)
		time.sleep_ms(1)
		for i in range(11):
			self.spi.send(self.RFConf[i])
		self.cs.value(1)
		
	def	txpacket(self,buf):
		self.cs.value(0)
		time.sleep_ms(1)
		self.spi.send(WTP)
		for i in range(len(buf)):
			self.spi.send(buf[i])
		self.cs.value(1)
		time.sleep_ms(1)
		self.cs.value(0)
		time.sleep_ms(1)
		self.spi.send(WTA)
		for i in range(4):
			self.spi.send(self.TxAddress[i])
		self.cs.value(1)
		time.sleep_ms(1)
		self.ce.value(1)
		time.sleep_ms(100)
		self.ce.value(0)
		
	def	setTXmode(self):
		self.ce.value(1)
		self.txen.value(1)
		time.sleep_ms(1)
		
	def	sender_bruff(self,buf):
		self.setTXmode()
		time.sleep_ms(10)
		self.txpacket(buf)
		time.sleep_ms(100)
		
	def	rxpacket(self):
		time.sleep_ms(100)
		self.cs.value(0)
		time.sleep_ms(1)
		self.spi.send(PRP)
		a=list(self.spi.recv(1))[0]
		rx_bruff=[]
		for i in range(a):
			rx_bruff.append(list(self.spi.recv(1))[0])
		self.cs.value(1)
		time.sleep_ms(100)
		self.ce.value(0)
		return rx_bruff
		
	def	checkDR(self):
		if	self.dr.value():
			return 1
		return 0
		
	def	setRXmode(self):
		self.txen.value(0)
		self.ce.value(1)
		time.sleep_ms(1)
		
	def	recvrx(self):
		self.setRXmode()
		while (self.checkDR()==0):
			a=0
		time.sleep_ms(100)
		return self.rxpacket()