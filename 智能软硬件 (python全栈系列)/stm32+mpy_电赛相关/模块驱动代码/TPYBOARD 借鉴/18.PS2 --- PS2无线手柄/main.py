# main.py -- put your code here!
import PS2

while True:
	ps=PS2.PS2KEY('X18','X19','X20','X21')
	a=ps.ps2_key()
	if(a==13):
		pyb.LED(1).on()
	elif(a==14):
		pyb.LED(2).on()
	elif(a==15):
		pyb.LED(3).on()
	elif(a==16):
		pyb.LED(4).on()
	elif(a==5):
		pyb.LED(1).off()
	elif(a==6):
		pyb.LED(2).off()
	elif(a==7):
		pyb.LED(3).off()
	elif(a==8):
		pyb.LED(4).off()
