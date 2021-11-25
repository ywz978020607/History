from machine import Pin,I2C
#base_addr : 扩展模块的i2c地址
#io_num : 读写的io引脚在模块种的标号0~7


class I2C_Pin():
    def __init__(self,i2c=None,Pin_scl = 19,Pin_sda = 21,base_addr = 33, freq= 300000):
        if not i2c:
            self.i2c = I2C(scl = Pin(Pin_scl),sda = Pin(Pin_sda),freq = freq)
        else:
            self.i2c = i2c

        self.base_addr = base_addr

    #io_num:[0,7]
    def value(self,io_num ,v = -1):
        data0 = self.i2c.readfrom(self.base_addr,1)[0]
        value = 1<<io_num
        if v == -1:
            return ((data0 & value)!=0)  #read &
        else:
            if v==0:
                data1 = data0 & (~value) #reset
            
            else:
                data1 = data0 | value   #set            

            self.i2c.writeto(self.base_addr,bytes([data1]))
            


