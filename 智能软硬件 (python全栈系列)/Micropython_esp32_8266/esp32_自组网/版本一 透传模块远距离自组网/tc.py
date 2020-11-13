from machine import Pin,UART

# 使用方式
# from tc import TC
# hc = TC()
# hc.send("abc")
# hc.recv()


class TC():
    def __init__(self,uart = 2,baudrate = 9600):
        self.u = UART(uart,baudrate) #
    
    def send(self,text):
        self.u.write(text)

    def recv(self):
        return self.u.read()


