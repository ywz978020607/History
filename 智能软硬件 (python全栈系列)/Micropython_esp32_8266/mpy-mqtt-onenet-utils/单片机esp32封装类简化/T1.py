from machine import *
import machine
import time
#wifi
import mywifi
import json
from simple import MQTTClient

#mqtt-class
class T1():
    SERVER = "183.230.40.39"
    get_data = {}
    def __init__(self,CLIENT_ID,username,password):
        self.CLIENT_ID = CLIENT_ID
        self.username = username
        self.password = password

    def wifi(self,SSID='ywzywz',PASS='12345678'):
        mywifi.WIFI(SSID=SSID,PASS=PASS)
    
    def mqttInit(self):
        self.c = MQTTClient(self.CLIENT_ID, self.SERVER,6002,self.username,self.password)
        # Subscribed messages will be delivered to this callback
        self.c.set_callback(self.sub_cb)
        self.c.connect()
        # self.c.subscribe(TOPIC_DOWN) #如果非$dp的其他主题
        # self.c.publish('$dp',pubdata([]))
        # c.publish(TOPIC_UP,pubdata())
        self.c.check_msg() #检测接收并调用sub_cb
        # c.wait_msg() #阻塞直到收到一次结束阻塞
    
    #整理上传格式--如果$dp主题
    def pubdata(self,data_name=[],data_value=[]):
        #arr是onenet的$dp主题
        # data = {'datastreams':[{'id':'temp','datapoints':[{'value':str(state)}] } ]}
        temp_list = []
        for ii in range(len(data_name)):
            temp_list.append({'id':data_name[ii],'datapoints':[{'value':data_value[ii]}]} )
            data = {'datastreams':temp_list}
            
        j_d = json.dumps(data)
        j_l = len(j_d)
        arr = bytearray(j_l + 3)
        arr[0] = 1 #publish数据类型为json
        arr[1] = int(j_l / 256) # json数据长度 高位字节
        arr[2] = j_l % 256      # json数据长度 低位字节
        arr[3:] = j_d.encode('ascii') # json数据
        return arr
        # return j_d  
      
    #上传-默认$dp主题
    def publish(self,TOPIC='$dp',mydict={}):
        if TOPIC=='$dp':
            data_name = list(mydict.keys())
            data_value = list(mydict.values())
            self.c.publish(TOPIC,self.pubdata(data_name,data_value))
        else:
            self.c.publish(TOPIC,json.dumps(mydict))

    #订阅并返回json--保存到self.get_data -- 调用使用Class.c.check_msg() 或wait_msg()
    def sub_cb(self,topic, msg):
        print((topic, msg))
        self.get_data = json.loads(msg)
        # print(self.get_data)
        # return self.get_data

