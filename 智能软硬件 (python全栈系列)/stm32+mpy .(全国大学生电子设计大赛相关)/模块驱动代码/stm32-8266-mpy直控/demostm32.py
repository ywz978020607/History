from pyb import UART,Pin
import time

addlast = "\r\n" #必须加
def getread(input): 
    try:
        #先decode成字符串
        input = input.decode()
        return input.split(addlast)[-2]
    except
        return ''

# 要设置read_buf_len
u = UART(2,115200,read_buf_len=500) #必须这个

name = ["data0","data1","data2","data3","switch"]
value = [1,1,2,3,0]

u.write("from t8266 import *"+addlast) #可能自动连 睡个10s
time.sleep(10)

def up():
    global name,value,addlast
    u.write("up("+str(name)+","+str(value)+") "+addlast) #可能自动连 睡个10s

def down():
    global val
    u.write("get() "+addlast) #可能自动连 睡个10s
    time.sleep(3)
    recv = u.read()

    recv = getread(recv)
    print(recv)
    get_data = json.loads(recv)
    val = get_data['datapoints'][4]
    print(val)
