from machine import I2C
from machine import Pin
import bma423 as bma

def handle_interrupt(pin):
	state = bma.read_irq()
	if state == bma.IRQ_STEP_COUNTER:
		s = bma.stepcount()
		print('IRQ_STEP_COUNTER %u' % s)
	elif state == bma.IRQ_DOUBLE_WAKEUP:
		print('IRQ_DOUBLE_WAKEUP')

i2c = I2C(scl=22, sda=21,speed=400000)
bma.init(i2c,irq=True)
irq = Pin(39, mode=Pin.IN,handler=handle_interrupt,trigger=Pin.IRQ_RISING)