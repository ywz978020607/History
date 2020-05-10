
import bigiot
ID = "12617"                             # 设备ID
API_KEY = "eca35b8e9"                        # 设备APIKEY

def recv(msg):
    print(msg)

device = bigiot.Device(ID, API_KEY)         # 构建bigiot 设备

device.say_callback(recv)                 # 设置say通讯的回调函数

device.check_in()   