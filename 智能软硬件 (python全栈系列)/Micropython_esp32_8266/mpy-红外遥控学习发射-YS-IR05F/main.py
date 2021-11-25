import machine
import time
import json
import urequests
from machine import Pin
from machine import UART
from config import *
# import mywifi 
import wifimgr
#########################################
# # check if the device woke from a deep sleep
# if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#     print('woke from a deep sleep')

###
def task1():
    u=UART(1,9600) #only tx can be used = Pin(2)
    c=config('data.ini')
    # u.read() #UART(1) can't read
    ret = c.readAll()

    # rtc = machine.RTC()
    # rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    
    # mywifi.WIFI()
    wlan = wifimgr.get_connection()
    #####
    #upload
    url="http://api.heclouds.com/devices/643534dxx/datapoints"
    headers={'api-key':'gjxxxxxxxxxxx'}
    data_name = ["lock"]
    data_value = [0] 
    def upload():
        # global data_name,data_value
        temp_list = []
        for ii in range(len(data_name)):
            # temp_list.append({'id':data_name[ii],'datapoints':[{'value':'%.1f' % data_value[ii]}]} )
            temp_list.append({'id':data_name[ii],'datapoints':[{'value': data_value[ii]}]} )
        data = {'datastreams':temp_list}
        rp = urequests.post(url, headers=headers, data=json.dumps(data))
        rp.close()
    #update
    # upload()

    ###
    def down():
        # global data_name,data_value
        r=urequests.get(url,headers=headers)
        data_value[0] = r.json()['data']['datastreams'][0]['datapoints'][0]['value']
        data_value[0] = (int)(data_value[0])
        r.close()  #esp32的urequest，记得关 close !!!
        
    #####
    while 1:
        try:
            print("start")
            down()
            if data_value[0] == 1 :
                print("open")
                u.write(ret['open'])
                data_value[0] = 0
                #update
                upload()
            elif data_value[0] == 2:
                print("close")
                u.write(ret['close'])
                data_value[0] = 0
                #update
                upload()
        except:
            print("error")
        time.sleep(5) #60
        machine.reset()
        # set RTC.ALARM0 to fire after 60 seconds (waking the device)
        # rtc.alarm(rtc.ALARM0, 10000)

        # put the device to sleep
        # machine.deepsleep()

##########################################
## __main__
task1()
