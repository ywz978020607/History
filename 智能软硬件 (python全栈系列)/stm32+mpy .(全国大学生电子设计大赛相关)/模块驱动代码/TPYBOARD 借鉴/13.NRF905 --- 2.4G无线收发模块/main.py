import nrf905
import time
from pyb import SPI

RFConf=[0x00,					#配置命令
		0x4c,					#频段设置为423Mhz
		0x0c,					#输出功率为10db，不重发，节电模式为正常
		0x44,					#地址宽度设置为4字节
		0x0a,0x0a,				#接收发送有效数据长度为3字节
		0xcc,0xcc,0xcc,0xcc,	#接收地址
		0x58					#CRC允许，8位CRC校验，外部时钟信号不使能
		]
TxAddress=[0xcc,0xcc,0xcc,0xcc]	#接收地址

buf=[0x06,0xa0,0xb0,0x01,0x02,0]	#发送内容

spi=pyb.SPI(2)
n=nrf905.NRF905(spi=spi,ce='Y1',txen='Y2',pwr='Y3',cd='Y4',dr='Y12',cs='Y11',
				RFConf=RFConf,TxAddress=TxAddress)
i=0
while True:
	buf[5]=i
	n.sender_bruff(buf)
	time.sleep_ms(200)
	print(i)
	i+=1
	
# import nrf905
# import time
# import pyb

# RFConf=[0x00,					#配置命令
		# 0x4c,					#频段设置为423Mhz
		# 0x0c,					#输出功率为10db，不重发，节电模式为正常
		# 0x44,					#地址宽度设置为4字节
		# 0x0a,0x0a,				#接收发送有效数据长度为3字节
		# 0xcc,0xcc,0xcc,0xcc,	#接收地址
		# 0x58					#CRC允许，8位CRC校验，外部时钟信号不使能
		# ]

# spi=pyb.SPI(2)
# n=nrf905.NRF905(spi=spi,ce='Y1',txen='Y2',pwr='Y3',cd='Y4',dr='X9',cs='X10',
				# RFConf=RFConf,TxAddress=None)
# while True:
	# buf=n.recvrx()
	# print (buf)