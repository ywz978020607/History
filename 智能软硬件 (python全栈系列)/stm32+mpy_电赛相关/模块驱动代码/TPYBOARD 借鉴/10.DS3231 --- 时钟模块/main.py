import machine
import time
from ds3231 import DS3231

ds=DS3231()
ds.DATE([17,9,1])
ds.TIME([10,10,10])

while True:
    print('Date:',ds.DATE())
    print('Time:',ds.TIME())
    print('TEMP:',ds.TEMP())
    time.sleep(5)