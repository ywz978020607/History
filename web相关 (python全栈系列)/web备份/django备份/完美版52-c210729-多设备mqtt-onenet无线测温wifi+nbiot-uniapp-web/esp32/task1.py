#esp32-mqtt-task1
from machine import *
import machine
import time
#wifi
import mywifi
import json
from simple import MQTTClient
import _thread 
import ssd1306

mywifi.WIFI(SSID='ywzywz',PASS='12345678')

def get_temp(ret_array):
    if len(ret_array)>11:
        ret_array = ret_array[-12:]
        if ret_array[0]==164: #b'\xa4'
            temp = (ret_array[-7]*256+ret_array[-6])/100
            return temp
    return None

# Default MQTT server to connect to
SERVER = "183.230.40.39"
CLIENT_ID = "755720734"
username='234533'
password='2kJV69eUrcMgCLjkyOzT8k1WY0Y='

get_data = {}

con1 = Pin(5,Pin.OUT)
con1.off()

#gy615
u1 = UART(1,rx=21,tx=19,baudrate=9600)
#nbiot
# u2 = UART(2,9600)

#oled
i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
oled=ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(0)
oled.text("hello",50,54)
oled.show()

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
    global con1 #,get_data
    print((topic, msg))
    # get_data = json.loads(msg)
    # print(get_data)
    if "on" in str(msg):
        con1.on()
    if "off" in str(msg):
        con1.off()

###init for mqtt
c = MQTTClient(CLIENT_ID, SERVER,6002,username,password)
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()

# c.publish('$dp',pubdata(10))
# c.check_msg() #检测接收并调用sub_cb
# c.wait_msg() #阻塞直到收到一次结束阻塞

def thread1():
    global c 
    while 1:
        try:
            c.wait_msg()
        except:
            print("msg error")
            
show_value = ["off","on"]
def task_main():
    global c,u1,oled,CLIENT_ID,con1,show_value

    temp = get_temp(u1.read())
    print(temp)
    #oled显示
    oled.fill(0)
    oled.text(CLIENT_ID,10,4)
    oled.text(str(temp),10,24)    
    oled.text(show_value[con1.value()],10,44)    
    oled.show()

    c.publish('$dp',pubdata(temp))

    # c.check_msg() #检测接收并调用sub_cb

def run():
    _thread.start_new_thread(thread1,())
    while 1:
        try:
            task_main()
            # time.sleep(5)
            time.sleep_ms(50)
        except:
            print("error")


