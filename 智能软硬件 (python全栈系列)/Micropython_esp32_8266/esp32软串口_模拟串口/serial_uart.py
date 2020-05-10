import time
import machine # Need to be Init
import serial

# >>> from serial_uart import uart
# >>> import time
# >>>
# >>> com = uart(27, 34, False, 512)  #tx=27, rx=34
# >>> com.open(9600)
# 0
# >>> com.write(b'abc')
# 3
# >>> com.read()
# b'qwe'


#little write
class uart:

    def __init__(self, tx=27, rx=34, Inverse=False, buffSize=512):
        self.port = serial.new(tx, rx, Inverse, buffSize)

    def __del__(self):
        # pass  # will reset
        serial.delete(self.port)

    def any(self):
        return serial.any(self.port)

    def open(self, baudRate):
        return serial.open(self.port, baudRate)

    def stop(self):
        return serial.stop(self.port)

    # def write(self, num):
    #     return serial.write(self.port, num[0])

    # def read(self):
    #     return  bytes([serial.read(self.port)])

    def write(self,num):
        for ii in range(len(num)):
            serial.write(self.port,num[ii])
        return len(num)

    def read(self):
        t=b''
        while self.any():
            t = t + bytes([serial.read(self.port)])
        return t 


