import pyb
from pyb import Pin, I2C

class AT24C0X:
    def __init__(self,spi):
        self.accel_addr = 80
        self.i2c = pyb.I2C(spi)
        self.i2c.init(pyb.I2C.MASTER, baudrate=400000)
        print(self.i2c.scan())

    def writeAT24C0X(self,addr,data):
        self.i2c.scan()
        self.i2c.is_ready(self.accel_addr)
        if isinstance(data,int):
            size=1
        else:
            size=int(len(data)/8)+1
        b=bytearray(data)
        for i in range(size):
            self.i2c.mem_write(b[i*8:i*8+8], self.accel_addr,0,timeout=1000, addr_size=8)

    def readAT24C0X(self,add,bit_len):
        self.i2c.scan()
        self.i2c.is_ready(self.accel_addr)
        self.data=self.i2c.mem_read(bit_len, self.accel_addr, add, timeout=1000,addr_size=8)
        return self.data