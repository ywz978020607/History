from machine import I2C,Pin
import time

#base_addr为扩展io模块的IIC地址

#readfrom(addr,byte_num)
#writeto(addr,valuebyte)

class matkey():
    _map={2:4,3:7,4:11,5:2,6:5,7:8,8:10,9:3,10:6,11:9}

    def __init__(self,i2c=None,Pin_scl = 'PG1',Pin_sda = 'PE7',Pin_led='PF9', freq= 300000 , base_addr = 32 ):  
        if not i2c:
            self.i2c = I2C(scl = Pin(Pin_scl),sda = Pin(Pin_sda),freq = freq)
        else:
            self.i2c = i2c
        self.base_addr = base_addr
        self.led=Pin(Pin_led,Pin.OUT)
        self.led.value(1)  #close

    def check_key(self):
        #先看行
        self.i2c.writeto(self.base_addr,b'\xf0')
        data = self.i2c.readfrom(self.base_addr,1)[0]  #int
        if data == 0xf0:
            return 0
        else:
            row = 0
            for ii in range(4):
                if (((data<<ii) & 0x80) ^0x80):
                    row = ii
                    break
            
            time.sleep_ms(20) 
            #再看列
            self.i2c.writeto(self.base_addr,b'\x0f')
            data = self.i2c.readfrom(self.base_addr,1)[0]  #int
            if data == 0x0f:
                return 0
            else:
                line = 0
                for ii in range(4):
                    if (((data<<ii) & 0x08)^0x08):
                        line = ii +1
                        break          
                return (row*4 + line)
            
    def check(self):
        button = self.check_key()
        if button!=0:
            self.led.off()  #open
            while self.check_key()==button:
                pass
            self.led.on()

            #new keyboard
            if button in self._map.keys():
                return self._map[button]
            else:
                return button
    
        else:
            return 0
