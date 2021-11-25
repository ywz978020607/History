from machine import UART
import time
import uos, machine

time.sleep(5)

#detach
uos.dupterm(None, 1)
### do sth with UART 0 
uart = UART(0, baudrate=9600)
for ii in range(10):
    uart.write(b'hello')
    time.sleep(2)
# uart.read(5) # read up to 5 bytes

#attach
uart = machine.UART(0, 115200)
uos.dupterm(uart, 1)


