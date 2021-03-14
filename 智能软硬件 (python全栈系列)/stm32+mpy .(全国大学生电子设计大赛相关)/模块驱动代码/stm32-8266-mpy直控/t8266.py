#task 8266

import mywifi
import urequests,json
import time

mywifi.WIFI()


#定义大量函数 在stm32端调用 任何print都是返回
#onenet
def up(data_name,data_value):
    try:
        url="http://api.heclouds.com/devices/692830839/datapoints"
        headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}

        temp_list = []
        for ii in range(len(data_name)):
            temp_list.append({'id':data_name[ii],'datapoints':[{'value':data_value[ii]}]} )
            
        data = {'datastreams':temp_list}
        rp = urequests.post(url, headers=headers, data=json.dumps(data))
        rp.close()
        print("ok")
    except:
        print('error')


def get():
    try:
        url="http://api.heclouds.com/devices/692830839/datapoints"
        headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}

        r=urequests.get(url,headers=headers)
        out = r.json()['data']['datastreams']
        print(json.dumps(out))
        r.close()

    except:
        print('error')

# """
# from t8266 import *
# import json
# name = ["data0","data1","data2","data3","switch"]
# value = [0,1,2,3,0]

# up(name,value)

# recv = get()
# json.loads(recv)
# """