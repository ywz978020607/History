from machine import Pin,UART
import struct

#a[0:len(b[0])]==b[0]
#get_cmd=b'\xee\xb1\x11\x00\x00\00\x02\xff\xfc\xff\xff'
#m.split(b'\xee')[-1].split(b'\xff\xfc\xff\xff')[0]

#切换到画面1：EE B1 00 00 01 FF FC FF FF  ||  b'\xee\xb1\x00\x00\x01\xff\xfc\xff\xff'
#文本框滚动：EE B1 16 00 01 00 01 00 32 FF FC FF FF  其中32对应速度

# 大佬让我过去吧 ： b'\xb4\xf3\xc0\xd0\xc8\xc3\xce\xd2\xb9\xfd\xc8\xa5\xb0\xc9'
# 祝您每天 b'\xd7\xa3\xc4\xfa\xc3\xbf\xcc\xec'
# 财源广进心想事成  b'\xb2\xc6\xd4\xb4\xb9\xe3\xbd\xf8\xd0\xc4\xcf\xeb\xca\xc2\xb3\xc9'

# 谢谢大佬 b'\xd0\xbb\xd0\xbb\xb4\xf3\xc0\xd0'
# 大佬最美 b'\xb4\xf3\xc0\xd0\xd7\xee\xc3\xc0'

# #设置蓝色 EE B1 19 00 01 00 01 06 7F FF FC FF FF 
# #设置红色 EE B1 19 00 01 00 01 F8 00 FF FC FF FF 
# #设置白色 EE B1 19 00 01 00 01 FF FF FF FC FF FF 


# u.set_text_bytestrings(1,1,b'\xb4\xf3\xc0\xd0\xc8\xc3\xce\xd2\xb9\xfd\xc8\xa5\xb0\xc9 \xd7\xa3\xc4\xfa\xc9\xed\xcc\xe5\xbd\xa1\xbf\xb5 \xb2\xc6\xd4\xb4\xb9\xe3\xbd\xf8')

# 速度
# u.set_text_scroll(1,1,0)

class UARTLCD():

    def __init__(self,com=1,baudrate=9600):
        self._uart = UART(com,baudrate)
        self._readbuff=b''
        # self.reset()

        
    def reset(self):
        self._uart.write(b'\xee\x07\x35\x5a\x53\xa5\xff\xfc\xff\xff')

    def change_screen(self,pic):
        send=b'\xee\xb1\x00' + struct.pack('>H',pic) + b'\xff\xfc\xff\xff' #>H =>1:\x00\x01
        self._uart.write(send)

    #文本框滚动
    def set_text_scroll(self,pic,id,speed):
        #speed=0不滚动
        send = send=b'\xee\xb1\x16' + struct.pack('>H',pic)+ struct.pack('>H',id)+ struct.pack('>H',speed) + b'\xff\xfc\xff\xff'
        self._uart.write(send)


    def check(self):
        ##mode 
        #0:button_back
        #1:text_back
        #2:button_pushed_back(status click)
        if self._uart.any():
            self._readbuff = self._readbuff + self._uart.read()
            back_list=[]
            recv = self._readbuff
            recv = recv.split(b'\xee')
            if len(recv)>1:
                recv=recv[-1].split(b'\xff\xfc\xff\xff')
                if len(recv)>1:
                    recv = recv[0] #最后一组的内容
                    #成功收到
                    print(recv)
                    self._readbuff=b''
                    ##button
                    if len(recv)==9 and recv[1:2] == b'\x11' and recv[6:9]==b'\x10\x01\x00':
                        back_list.append(0)
                        back_list.append(16*recv[2]+recv[3])
                        back_list.append(16*recv[4]+recv[5])
                        return back_list
                    
                    #text
                    elif len(recv)>8 and recv[1:2]==b'\x11' and recv[6:7] == b'\x11':
                        back_list.append(1)
                        back_list.append(16*recv[2]+recv[3])
                        back_list.append(16*recv[4]+recv[5])
                        back_list.append(recv[7:-1].decode())
                        return back_list
                    
                    ##button_pushed(status)
                    if len(recv)==9 and recv[1:2] == b'\x11' and recv[6:9]==b'\x10\x01\x01':
                        back_list.append(2)
                        back_list.append(16*recv[2]+recv[3])
                        back_list.append(16*recv[4]+recv[5])
                        return back_list
                    
        return None
        
    #写文本框命令
    def set_text(self,pic,id,text):
        #str -> bytearray
        send=b'\xee\xb1\x10' + struct.pack('>H',pic) + struct.pack('>H',id) + text.encode() + b'\xff\xfc\xff\xff'
        self._uart.write(send)
    
    #mpy不自带转gb2312，除非将中文文件夹存为gb2312格式编码，建议直接联服务器通信传输字节，或提前在电脑端转后直接写入gb2312中文字节流
    def set_text_bytestrings(self,pic,id,bytestrings):
        #bytearray
        send=b'\xee\xb1\x10' + struct.pack('>H',pic) + struct.pack('>H',id) + bytestrings + b'\xff\xfc\xff\xff'
        self._uart.write(send)
    
    def set_text_color(self,pic,id,color):
        #color=0:白色  1：红色  2 ：蓝色
        if color==0:
            send = b'\xee\xb1\x19' + struct.pack('>H',pic) + struct.pack('>H',id) + b'\xff\xff' + b'\xff\xfc\xff\xff'
        elif color==1:
            send = b'\xee\xb1\x19' + struct.pack('>H',pic) + struct.pack('>H',id) + b'\xf8\x00' + b'\xff\xfc\xff\xff'
        elif color==2:
            send = b'\xee\xb1\x19' + struct.pack('>H',pic) + struct.pack('>H',id) + b'\x06\x7f' + b'\xff\xfc\xff\xff'
        
        self._uart.write(send)

    #读文本框命令
    def cmd_read_text(self,pic,id):
        send = b'\xee\xb1\x11' + struct.pack('>H',pic) + struct.pack('>H',id) + b'\xff\xfc\xff\xff'
        self._uart.write(send)
    
    def clear_graph(self,pic,id,channel):
        send = b'\xee\xb1\x33' + struct.pack('>H',pic) + struct.pack('>H',id) + struct.pack('B',channel) + b'\xff\xfc\xff\xff'
        self._uart.write(send)

    def add_point(self,pic,id,channel,data,byte=1):
        if byte==1:
            send = b'\xee\xb1\x35' + struct.pack('>H',pic) + struct.pack('>H',id) + struct.pack('B',channel) + b'\x00\x01' + struct.pack('B',data) + b'\xff\xfc\xff\xff'
            self._uart.write(send)
    
    def add_all_point(self,pic,id,channel,data,byte=1): #data is a bytearray
        if byte==1:
            send = b'\xee\xb1\x35' + struct.pack('>H',pic) + struct.pack('>H',id) + struct.pack('B',channel) + struct.pack('>H',len(data)) + data + b'\xff\xfc\xff\xff'
        elif byte==2:
            data_n = b''
            for jj in range(len(data)):
                data_n = data_n + struct.pack('>H',data[jj])
            send = b'\xee\xb1\x35' + struct.pack('>H',pic) + struct.pack('>H',id) + struct.pack('B',channel) + struct.pack('>H',len(data_n)) + data_n + b'\xff\xfc\xff\xff'
        self._uart.write(send)

    #播放sd卡中的音乐
    #s.lcd._uart.write(b'\xEE\x94\x53\x44\x3A\x2F\x30\x32\x2E\x6D\x70\x33\xFF\xFC\xFF\xFF')  
    #SD-> 02.mp3