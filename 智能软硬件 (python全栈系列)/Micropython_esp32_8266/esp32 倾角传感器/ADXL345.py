from machine import Pin
from machine import I2C
import time
import ustruct
import math


DATA_FORMAT = 0x31
BW_RATE  = 0x2c
POWER_CTL = 0x2d
INT_ENABLE  = 0x2E
OFSX = 0x1e
OFSY =0x1f
OFSZ =0x20

class adxl345:
    def __init__(self, scl, sda, cs):
        self.scl = scl
        self.sda = sda
        self.cs = cs
        cs.value(1)
        time.sleep(1)
        self.i2c = I2C(scl = self.scl, sda = self.sda, freq = 10000)
        slv = self.i2c.scan()
        print(slv)
        for s in slv:
            buf = self.i2c.readfrom_mem(s, 0, 1)
            print(buf)
            if(buf[0] == 0xe5):
                self.slvAddr = s
                print('adxl345 found')
                break
        #self.writeByte(POWER_CTL,0x00)  #sleep
        #time.sleep(0.001)
        #低电平中断输出,13位全分辨率,输出数据右对齐,16g量程
        self.writeByte(DATA_FORMAT,0x2B)
        #数据输出速度为100Hz
        self.writeByte(BW_RATE,0x0A)
        #不使用中断
        self.writeByte(INT_ENABLE,0x00)

        self.writeByte(OFSX,0x00)
        self.writeByte(OFSY,0x00)
        self.writeByte(OFSZ,0x00)
        #链接使能,测量模式
        self.writeByte(POWER_CTL,0x28)
        time.sleep(1)

    def readXYZ(self):
        fmt = '<h' #little-endian
        buf1 = self.readByte(0x32)
        buf2 = self.readByte(0x33)
        buf = bytearray([buf1[0], buf2[0]])
        x, = ustruct.unpack(fmt, buf)
        x = x*3.9
        #print('x:',x)

        buf1 = self.readByte(0x34)
        buf2 = self.readByte(0x35)
        buf = bytearray([buf1[0], buf2[0]])
        y, = ustruct.unpack(fmt, buf)
        y = y*3.9
        #print('y:',y)

        buf1 = self.readByte(0x36)
        buf2 = self.readByte(0x37)
        buf = bytearray([buf1[0], buf2[0]])
        z, = ustruct.unpack(fmt, buf)
        z = z*3.9
        #print('z:',z)
        #print('************************')
        #time.sleep(0.5)
        return (x,y,z)

    def writeByte(self, addr, data):
        d = bytearray([data])
        self.i2c.writeto_mem(self.slvAddr, addr, d)
    def readByte(self, addr):
        return self.i2c.readfrom_mem(self.slvAddr, addr, 1)


    def RP_calculate(self):
        x,y,z = self.readXYZ()

        roll = math.atan2(y , z) * 57.3
        pitch = math.atan2((- x) , math.sqrt(y * y + z * z)) * 57.3
        return roll,pitch

# scl = Pin(26)
# sda = Pin(25)
# cs = Pin(33, Pin.OUT)
# snsr = adxl345(scl, sda, cs)
# while True:
#     x,y,z = snsr.readXYZ()
#     snsr.RP_calculate()
#     print('x:',x,'y:',y,'z:',z,'uint:mg')
#     time.sleep(0.5)
