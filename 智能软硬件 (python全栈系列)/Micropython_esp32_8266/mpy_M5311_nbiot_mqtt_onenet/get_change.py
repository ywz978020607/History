import struct
import json
#针对onenete mqtt 发送的字节转换
# http://www.luyixian.cn/news_show_240809.aspx

# from get_change import *
# k={'1':1,'2':1,'3':1,'4':1}
# k1 = get_type(k)
# print(k1)

def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

def get_type(context): #context={'1':1,...} #尽量不要带空格
    temp = json.dumps(context)
    temp = temp.replace(', ',',')
    temp = temp.replace(': ',':')
    
    len1 = len(temp)
    str_hex_len1 = hex(len1)[2:] #eg:'19'
    #补全为4个显示,0019
    str_hex_len1 = '0'*(4-len(str_hex_len1)) + str_hex_len1

    len2 = len1 + 3
    str_len2 = str(len2)

    temp2 = ByteToHex(temp.encode()).encode()


    ret = str_len2.encode() +b',03'+ str_hex_len1.encode() + temp2

    return ret

