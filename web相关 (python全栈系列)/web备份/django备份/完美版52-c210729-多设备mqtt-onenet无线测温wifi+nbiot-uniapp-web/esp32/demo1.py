#esp32-mqtt-task1
from machine import *
import machine
import time
#wifi
import mywifi
import json
from simple import MQTTClient

mywifi.WIFI(SSID='ywzywz',PASS='12345678')

# Default MQTT server to connect to
SERVER = "183.230.40.39"
CLIENT_ID = "755720734"
TOPIC_UP = "topic1"
TOPIC_DOWN = "topic1down"

username='234533'
password='2kJV69eUrcMgCLjkyOzT8k1WY0Y='
state = 10

get_data = {}

def pubdata(state):
    # global state
    #注释的是onenet的$dp主题
    data = {'datastreams':[{'id':'temp','datapoints':[{'value':str(state)}] } ]}
    j_d = json.dumps(data)
    j_l = len(j_d)
    arr = bytearray(j_l + 3)
    arr[0] = 1 #publish数据类型为json
    arr[1] = int(j_l / 256) # json数据长度 高位字节
    arr[2] = j_l % 256      # json数据长度 低位字节
    arr[3:] = j_d.encode('ascii') # json数据
    return arr
    # data = {'name':'001','data':[10.46,35.4,0,1]}
    # j_d = json.dumps(data)
    # return j_d

def sub_cb(topic, msg):
    global state,get_data
    print((topic, msg))
    get_data = json.loads(msg)
    print(get_data)

###init for mqtt
c = MQTTClient(CLIENT_ID, SERVER,6002,username,password)
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()
c.subscribe(TOPIC_DOWN)
c.publish('$dp',pubdata(15))
# c.publish(TOPIC_UP,pubdata())
c.check_msg() #检测接收并调用sub_cb
# c.wait_msg() #阻塞直到收到一次结束阻塞

def task_main():
    global c,TOPIC_UP

    c.publish('$dp',pubdata(15))
    # c.publish(TOPIC_UP,pubdata())
    
    c.check_msg() #检测接收并调用sub_cb

def run():
    while 1:
        task_main()
        time.sleep(5)



