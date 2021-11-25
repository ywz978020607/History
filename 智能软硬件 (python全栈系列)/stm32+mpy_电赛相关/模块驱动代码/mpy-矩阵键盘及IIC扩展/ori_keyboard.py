from machine import Pin
import time

# >>>>>>>>>>
# 
# from machine import Pin
# from ori_keyboard import *
# key_list_name = ["PD0","PD1","PD2","PD3","PD4","PD5","PD6","PD7"]
# key_list = []
# for ii in range(8):
#     key_list.append(Pin(key_list_name[ii], Pin.OUT))
# key_mat = matkey(key_list) 
# key_mat.check()


class matkey():
    _map={2:4,3:7,4:10,5:2,6:5,7:8,8:11,9:3,10:6,11:9}
    def __init__(self):  
        # self.key_list = key_list
        self.key_list_name = ["PD0","PD1","PD2","PD3","PD4","PD5","PD6","PD7"]
        self.key_list = []
        for ii in range(8):
            self.key_list.append(0)

    def check_key(self):
        ###############################
        row = 0
        line = 0
        #先看行
        for ii in range(4):
            # self.key_list[ii].on()
            # self.key_list[ii+4].off()
            self.key_list[ii] = Pin(self.key_list_name[ii],Pin.IN,Pin.PULL_DOWN)
            self.key_list[ii+4] = Pin(self.key_list_name[ii+4],Pin.OUT,Pin.PULL_UP)
            self.key_list[ii+4].on() 
        for ii in range(4):
            if self.key_list[ii].value() == 1:
                row = ii
                break
        time.sleep_ms(200) 
        # print(row)
        #再看列
        
        for ii in range(4):
            # self.key_list[ii+4].on()
            # self.key_list[ii].off()
            self.key_list[ii+4] = Pin(self.key_list_name[ii+4],Pin.IN,Pin.PULL_DOWN)
            self.key_list[ii] = Pin(self.key_list_name[ii],Pin.OUT,Pin.PULL_UP)
            self.key_list[ii].on()
        time.sleep_ms(200) 
        for ii in range(4):
            if self.key_list[ii+4].value() == 1:
                line = ii +1 #1->16
                break          
        # print(line)
        return (row*4 + line)
            

    def check(self):
        button = self.check_key()
        if button!=0:
            # self.led.off()  #open
            while 1:
                temp = self.check_key()
                if temp == 0:
                    break
                if temp>button:
                    button = temp
            # self.led.on()

            #new keyboard
            if button in self._map.keys():
                return self._map[button]
            else:
                return button
    
        else:
            return 0

    def val(self):
        for ii in range(8):
            print(self.key_list[ii].value())