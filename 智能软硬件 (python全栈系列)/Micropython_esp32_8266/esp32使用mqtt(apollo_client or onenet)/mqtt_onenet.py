from simple import MQTTClient
from machine import Pin
import time
import machine
import json
import micropython
import _thread

class Product():
    def __init__(self,server="183.230.40.39",client_id="524485249",port=6002,topic=b"topic1",username='234533',password='2kJV69eUrcMgCLjkyOzT8k1WY0Y=',check=1):
        # Default MQTT server to connect to
        self.SERVER = server
        self.CLIENT_ID = client_id
        self.TOPIC = topic
        self.PORT = port
        self.username = username
        self.password = password
        #上传数据变量
        self.value_data = 0

        self.c = MQTTClient(self.CLIENT_ID, self.SERVER,self.PORT,self.username,self.password)
        self.c.set_callback(self.sub_cb)
        self.c.connect()
        self.c.subscribe(self.TOPIC)
        self.c.publish('$dp',self.pubdata("temp0",self.value_data)) #上传

        
        if check == 1:
            _thread.start_new_thread(self.keep_alive,())

        _thread.start_new_thread(self.wait_listen,())



    def keep_alive(self):
        while 1:
            #self.c.publish('$dp',self.pubdata()) #上传
            self.c.ping()
            time.sleep(30)

    def wait_listen(self):
        while 1:
            self.c.wait_msg()

    def pubdata(self,id,up_data):
        data = {'datastreams':[{'id':str(id),'datapoints':[{'value':str(up_data)}] } ]}
        j_d = json.dumps(data)
        j_l = len(j_d)
        arr = bytearray(j_l + 3)
        arr[0] = 1 #publish数据类型为json
        arr[1] = int(j_l / 256) # json数据长度 高位字节
        arr[2] = j_l % 256      # json数据长度 低位字节
        arr[3:] = j_d.encode('ascii') # json数据
        return arr


    def sub_cb(self,topic, msg):
        print((topic, msg))
        if msg == b"off":
            print("1")
        elif msg == b"on":
            print("0")

