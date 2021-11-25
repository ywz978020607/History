###转换的函数 from test1 import *

import struct

def set_name(name):#str
    temp_data = b''
    if len(name)<=8:
        for ii in range(8-len(name)):
            temp_data +=  b'\x00'
        temp_data += name.encode()
        # temp_data += bytes(8)
        return temp_data

def get_name(code): #bytes,int[]
    temp_name = ''
    for ii in range(8):
        if code[ii] != 0:
            temp_name += chr(code[ii])
    return temp_name


def get_bytes(code): #int[]
    temp_res = b''
    for ii in range(16):
        temp_res += struct.pack('B',code[ii])
    return temp_res

def set_value(val): #<25.6
    temp_val = (int)(val*10)
    if temp_val>255:
        temp_val = 255
    temp_byte = struct.pack('B',temp_val)
    return temp_byte

def read_value(val): #1 byte
    return val[0]/10


