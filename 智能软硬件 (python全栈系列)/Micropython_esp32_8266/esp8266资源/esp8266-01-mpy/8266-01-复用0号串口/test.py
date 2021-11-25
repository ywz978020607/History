#esp32 test
from machine import UART
import time

u=UART(2,9600)
while 1:
    recv = u.read()
    print(recv)
    time.sleep(1)

