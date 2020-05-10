from pyb import UART

def sendspeak(uart,baud,data):
	u2=UART(uart,baud)
	eec=0
	buf=[0xfd,0x00,0,0x01,0x01]
	buf[2]=len(data)+3
	buf+=list(data)
	for i in range(len(buf)):
		eec^=int(buf[i])
	buf.append(eec)
	u2.write(bytearray(buf))

# while True:
	# sendspeak(2,9600,'±Ï¼ªÌÎºÜÓÅ Ðã'.encode('utf-16'))
	# while True:
		# a=0