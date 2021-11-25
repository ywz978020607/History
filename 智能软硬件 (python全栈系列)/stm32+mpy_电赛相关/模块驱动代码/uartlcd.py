from machine import Pin,UART
import struct

#a[0:len(b[0])]==b[0]
#get_cmd=b'\xee\xb1\x11\x00\x00\00\x02\xff\xfc\xff\xff'
#m.split(b'\xee')[-1].split(b'\xff\xfc\xff\xff')[0]

#切换到画面1：EE B1 00 00 01 FF FC FF FF 
#文本框滚动：EE B1 16 00 01 00 01 00 32 FF FC FF FF  其中32对应速度


class UARTLCD():

    def __init__(self,com=1,baudrate=9600):
        self._uart = UART(com,baudrate)
        self._readbuff=b''
        self.reset()

        
    def reset(self):
        self._uart.write(b'\xee\x07\x35\x5a\x53\xa5\xff\xfc\xff\xff')


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