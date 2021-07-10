from pyb import UART
import time

class GY39:
	def __init__(self,uart):
		self.uart = UART(uart, 9600)

	def read(self):
		self.uart.read()
		time.sleep_ms(10)
		hc=self.uart.read()
		# hex_array = []
		# for i in list(hc):
		   # hex_array.append('%02X'%i)
		# print(hex_array,hex_array[0])

		l=(hc[4]<<24)|(hc[5]<<16)|(hc[6]<<8)|hc[9]
		t=((hc[13]<<8)|hc[14])/100
		p=((hc[15]<<24)|(hc[16]<<16)|(hc[17]<<8)|hc[18])/100
		h=((hc[19]<<8)|hc[20])/100
		H=((hc[21]<<8)|hc[22])
		return l,t,p,h,H