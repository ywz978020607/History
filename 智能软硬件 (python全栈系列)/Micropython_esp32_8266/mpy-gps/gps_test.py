from machine import Pin,I2C
import time
import ssd1306
import machine
from micropyGPS import MicropyGPS 


com = machine.UART(2,9600,timeout=10) #定义uart2
my_gps = MicropyGPS(8)#东八区的修正
my_gps.local_offset

gps_values = 'abc'
rtc = 'efg'
 
def get_GPS_values():    
    global gps_values,rtc #定义两个全局变量
    time.sleep(2)
    cc = com.readline()
    print(cc)
    for x in cc:
        my_gps.update(chr(x))
    #lat&long
    print(my_gps.latitude[0])
    gps_values = str(my_gps.latitude[0] + (my_gps.latitude[1] / 60)) + ',' + str(my_gps.longitude[0] + (my_gps.longitude[1] / 60))
    #datetime
    date = my_gps.date
    timestamp = my_gps.timestamp
    hour = timestamp[0]
    rtc = str(int(timestamp[0]))+":"+str(int(timestamp[1]))+":"+str(int(timestamp[2])) 
    return gps_values,rtc
 
while 1:
 
  time.sleep_ms(20)
  get_GPS_values()
  time.sleep_ms(100)
  print(gps_values) #本地调试，可删除
  print(rtc)#可删除[/font][/align][align=left][font=宋体]
  
  
  