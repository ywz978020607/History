# https://docs.micropython.org/en/latest/esp8266/quickref.html#
# UART0:UART0 is on Pins 1 (TX) and 3 (RX)

# When UART0 is attached to the REPL, 
# all incoming chars on UART(0) go straight to stdin so uart.read() 
# will always return None. 
# Use sys.stdin.read() if it’s needed to read characters from the UART(0) 
# while it’s also used for the REPL (or detach, read, then reattach). 
# When detached the UART(0) can be used for other purposes.
import sys
sys.stdin.read()
# read读取数据 ctrl+d是结束输入 ,read并不会像input那样遇到回车就返回读取的数据
# 它会缓存 #####或者 等到ctrl d再读取数据
###########################################################

#To detach the REPL from UART0, use:
import uos
uos.dupterm(None, 1)

##read
from machine import UART
uart = UART(0, baudrate=9600)
uart.write('hello')
uart.read(5) # read up to 5 bytes

# reattach
# The REPL is attached by default. If you have detached it, to reattach it use:

import uos, machine
uart = machine.UART(0, 115200)
uos.dupterm(uart, 1)


