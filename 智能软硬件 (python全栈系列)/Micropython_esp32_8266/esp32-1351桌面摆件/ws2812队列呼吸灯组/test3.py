#设计动画+渐变 
import random
import time

from machine import SPI,Pin
from ws2812 import *
from machine import ADC,Pin

import time

import _thread

#亮度衰减
decay = 10
num = 16

spi = SPI(1)
spi.init(baudrate=3200000,mosi=Pin(23))

chain = WS2812(spi,led_count=num)

data=[
    (0,0,0)
] * num
chain.show(data)
color_val = [128,128,128]

color_num = num
color_list = [False]*num

def write_color():
    #统一改变
    global chain,color_val,data,decay,num,color_num,color_list
    
    color = (color_val[0]//decay,color_val[1]//decay,color_val[2]//decay)
    black = (0,0,0)

    # color_num = get_color_num()
    # data.append((color_val[0]//decay,color_val[1]//decay,color_val[2]//decay))
    # data = [color] * color_num + [black] * (num-color_num) #统一改变
    for ii in range(num):
        data[ii] = (color_val[0]//decay,color_val[1]//decay,color_val[2]//decay) if color_list[ii] else black
    
    chain.show(data)


def get_index():
    return [(int)(random.random()*3-0.5),(int)(random.random()*3-0.5),(int)(random.random()*3-0.5)]

def change_color(final_val):
    global color_val,color_num
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



#第二线程检测adc
def thread_num():
    global chain,num,color_num,color_list
    while 1:
        # =================
        #3灯1组正转一圈对应range16
        color_list = [True]*3 + [False]*(num-3)    
        for ii in range(16*5):
            time.sleep_ms(50)
            #头补尾
            color_list.append(color_list.pop(0))
        # =================

        # =================
        #3灯1组反转一圈
        color_list = [True]*3 + [False]*(num-3)    
        for ii in range(16*5):
            time.sleep_ms(50)
            #尾补头
            temp = color_list[-1]
            color_list[1:]=color_list[0:-1]
            color_list[0] = temp    
        # =================
        # =================
        #3灯1组反转一圈
        color_list = [True]*3 + [False]*(num-3)    
        for ii in range(16):
            time.sleep_ms(100)
            #尾补头
            temp = color_list[-1]
            color_list[1:]=color_list[0:-1]
            color_list[0] = temp    
        # =================


_thread.start_new_thread(thread_num,())

main()



