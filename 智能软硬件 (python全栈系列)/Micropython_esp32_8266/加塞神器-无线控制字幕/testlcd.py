# repl>> execfile('testlcd.py')

from uartlcd import *
import time
text=[
    b'\xb4\xf3\xc0\xd0\xc8\xc3\xce\xd2\xb9\xfd\xc8\xa5\xb0\xc9',
    b'\xd7\xa3\xc4\xfa\xc3\xbf\xcc\xec',
    b'\xb2\xc6\xd4\xb4\xb9\xe3\xbd\xf8\xd0\xc4\xcf\xeb\xca\xc2\xb3\xc9',

    b'\xd0\xbb\xd0\xbb\xb4\xf3\xc0\xd0',
    b'\xb4\xf3\xc0\xd0\xd7\xee\xc3\xc0',
    b'\xd0\xc2\xc4\xea\xbf\xec\xc0\xd6\xb6\xaf\xcd\xbc\xb6\xa9\xd6\xc6'
]


u=UARTLCD(com=2)
time.sleep(1)
u.change_screen(1)
time.sleep(1)
print('start')

def act1():
    global u
    u.set_text_color(1,1,0)# 白色
    u.set_text_bytestrings(1,1,text[0])
    time.sleep(2)
    u.set_text_bytestrings(1,1,text[1])
    time.sleep(0.5)
    u.set_text_bytestrings(1,1,text[2])
    time.sleep(1)

########################
def act2():
    global u
    u.set_text_color(1,1,2) #蓝色
    u.set_text_bytestrings(1,1,text[3])
    time.sleep(2)

    u.set_text_color(1,1,1) #红色
    u.set_text_bytestrings(1,1,text[4])
    time.sleep(2)

def act3():
    global u
    u.set_text_color(1,1,1) #红色
    u.set_text_bytestrings(1,1,text[5])
    time.sleep(2)


##
if __name__=="__main__":
    act1()
    act2()

