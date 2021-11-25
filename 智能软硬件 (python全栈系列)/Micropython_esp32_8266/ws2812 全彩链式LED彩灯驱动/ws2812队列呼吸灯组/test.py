import random
import time

from machine import SPI,Pin
from ws2812 import *

#亮度衰减
decay = 10


spi = SPI(1)
spi.init(baudrate=3200000,mosi=Pin(23))

chain = WS2812(spi,led_count=8)

data=[
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
    (0,0,0),
]
chain.show(data)
color_val = [128,128,128]


def write_color():
    #队列式
    global chain,color_val,data,decay
    data.pop(0)
    data.append((color_val[0]//decay,color_val[1]//decay,color_val[2]//decay))
    chain.show(data)


def get_index():
    return [(int)(random.random()*3-0.5),(int)(random.random()*3-0.5),(int)(random.random()*3-0.5)]

def change_color(final_val):
    global color_val
    flag_list = [0,0,0]
    for ii in range(3):
        if final_val[ii]>color_val[ii]:
            flag_list[ii]=1
        elif final_val[ii]<color_val[ii]:
            flag_list[ii]=-1
        else:
            pass
    
    for ii in range(128):
        for jj in range(3):
            color_val[jj]+=flag_list[jj]
        #写入color_val
        write_color()
        # print(color_val)
        time.sleep_ms(100)


def cal_val():
    global color_val
    flag= True
    while flag:
        temp_index = get_index()
        if temp_index!=[1,1,1]:
            
            #0 up 1 down
            # final_val = copy.deepcopy(color_val)
            final_val = [color_val[0],color_val[1],color_val[2]]
            for ii in range(3):
                final_val[ii] = int(final_val[ii] + 128*(temp_index[ii]-1))
                final_val[ii] = final_val[ii] % 256
            if final_val!=[0,0,0] and final_val!=[255,255,255]:
                flag = False
    # print(temp_index)
    # print(final_val)
    change_color(final_val)


def main():
    while 1:
        cal_val()

