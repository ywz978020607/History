import machine
import time
import json
import urequests
from machine import Pin
import mywifi 

mywifi.WIFI()
#######################
time.sleep(2)
##########################

out = Pin(2,Pin.OUT)
def open():
    global out
    out.off()
def close():
    global out
    out.on()
close()
#####
#upload
url="http://api.heclouds.com/devices/611890860/datapoints"
headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}
data_name = ["lock"]
data_value = [0] 
def upload():
    global data_name,data_value
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
    global data_name,data_value
    r=urequests.get(url,headers=headers)
    data_value[0] = r.json()['data']['datastreams'][0]['datapoints'][0]['value']
    data_value[0] = (int)(data_value[0])
    r.close()  #esp32的urequest，记得关 close !!!
    
#####
while 1:
    try:
        down()
        if data_value[0] >0 :
            print("open")
            open()
            time.sleep(data_value[0]) #一般是1s  强制关机5~6s
            close()
            data_value[0] = 0
            #update
            upload()
    except:
        print("error")
    time.sleep(60)