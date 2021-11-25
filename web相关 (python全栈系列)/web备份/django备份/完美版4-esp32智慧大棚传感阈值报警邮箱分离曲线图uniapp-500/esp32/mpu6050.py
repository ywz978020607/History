import machine
import math
class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
            
    ##
    def dist(self,a,b):
       return math.sqrt((a*a)+(b*b))

    def get_x_rotation(self,x,y,z):
        radians = math.atan(x / self.dist(y,z))
        return math.degrees(radians)

    def get_y_rotation(self,x,y,z):
        radians = math.atan(y / self.dist(x,z))
        return math.degrees(radians)

    def get_angle(self):
        ret = self.get_values()
        x_scaled = ret['AcX'] / 16384.0
        y_scaled = ret['AcY'] / 16384.0
        z_scaled = ret['AcZ'] / 16384.0

        x_angle = self.get_x_rotation(x_scaled,y_scaled,z_scaled)
        y_angle = self.get_y_rotation(x_scaled,y_scaled,z_scaled)

        return x_angle,y_angle

    #x y倾角--整体平面倾角
    def get_dip(self):
        ret = self.get_values()
        x_scaled = ret['AcX'] / 16384.0
        y_scaled = ret['AcY'] / 16384.0
        z_scaled = ret['AcZ'] / 16384.0

        x_radians = math.atan(x_scaled / self.dist(y_scaled,z_scaled))
        y_radians = math.atan(y_scaled / self.dist(x_scaled,z_scaled))

        dip_radians = math.asin((math.sin(x_radians))**2 + (math.sin(y_radians))**2)
        return math.degrees(dip_radians)


    def test1(self):
        from time import sleep
        while 1:
            print(self.get_angle())
            sleep(0.05)
    
    def test2(self):
        from time import sleep
        while 1:
            print(self.get_dip())
            sleep(0.05)
    