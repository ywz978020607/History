from pyb import UART,Pin
import time
import json

addlast = "\r\n" #必须加
def getread(input): 
    try:
        #先decode成字符串
        input = input.decode()
        return input.split(addlast)[-2]
    except:
        return ''

# 要设置read_buf_len
u = UART(2,115200,read_buf_len=500) #必须这个

u.write("from t8266 import *"+addlast) #可能自动连 睡个10s
time.sleep(3)

data={"name":"001","data":[0,0,0,0,0,0,0]}
# get_data = {}
def up(data):
    global addlast #,get_data
    u.write("up("+str(data)+") "+addlast) #可能自动连 睡个10s
    time.sleep(3)
    recv = u.read()

    recv = getread(recv)
    print(recv)
    get_data = json.loads(recv)
    return get_data

def down(data):
    global addlast #,get_data
    u.write("down("+str(data)+") "+addlast) #可能自动连 睡个10s
    time.sleep(3)
    recv = u.read()

    recv = getread(recv)
    print(recv)
    get_data = json.loads(recv)
    return get_data