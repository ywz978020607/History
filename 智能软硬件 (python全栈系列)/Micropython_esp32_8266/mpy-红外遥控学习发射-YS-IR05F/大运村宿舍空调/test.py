#esp32 learn and save test

from machine import UART
import time
from config import *

u=UART(2,9600)
c=config('data.ini')
u.read()

# ret = {}
ret = c.readAll()

recv = u.read()
# if recv:
ret['close'] = recv
c.writeConfig(ret)
print('save')


while 1:
    recv = u.read()
    print(recv)
    time.sleep(1)

#use
ret = c.readAll()
u.write(ret['open'])
print(u.read())

ret = c.readAll()
u.write(ret['close'])
print(u.read())


# #change_key
# ret = c.readAll()
# ret['open'] = ret['close']
# ret.pop('close')
# c.writeConfig(ret)
