"""Test for nrf24l01 module.  Portable between MicroPython targets."""
import ustruct as struct
import utime
from pyb import Pin, SPI
from nrf24l01 import NRF24L01

pipes = (b'\xf0\xf0\xf0\xf0\xe1', b'\xf0\xf0\xf0\xf0\xd2')

class nrf24l01:
	def	__init__(self,spi,csn,ce):
		csn0 = Pin(csn, mode=Pin.OUT, value=1)
		ce0 = Pin(ce, mode=Pin.OUT, value=0)
		self.nrf = NRF24L01(SPI(spi), csn0, ce0, payload_size=8)

	def master(self,data):
		self.nrf.open_tx_pipe(pipes[0])
		self.nrf.open_rx_pipe(1, pipes[1])
		self.nrf.stop_listening()
		try:	
			self.nrf.send(struct.pack('i', data))	#发送内容 pack为封包函数
			self.nrf.start_listening()
			start_time = utime.ticks_ms()
			timeout = False
			while not self.nrf.any() and not timeout:
				if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
					timeout = True
		except OSError:
			pass
			
	def slave(self):
		self.nrf.open_tx_pipe(pipes[1])
		self.nrf.open_rx_pipe(1, pipes[0])
		self.nrf.start_listening()
		while True:
			if self.nrf.any():
				while self.nrf.any():
					buf = self.nrf.recv()							#接收内容
					data,a= struct.unpack('ii', buf)#解析包unpack为解析包函数
				break
		return data