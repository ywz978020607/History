# main.py -- put your code here!
import pyb
from pyb import Pin

Pin_All=[Pin(p,Pin.OUT_PP) for p in ['X1','X2','X3','X4']]
STEPER_ROUND=512 #转动一圈(360度)的周期
ANGLE_PER_ROUND=STEPER_ROUND/360 #转动1度的周期

class SteperMotor():

    def __init__(self,pin = None,speed=2):
        if pin != None:
            self.Pins = pin
        else:
            self.Pins = Pin_All
        self.Speed =  speed
    #私有方法
    def __SteperWriteData(self,data):
        count=0
        for i in data:
            self.Pins[count].value(i)
            count+=1
    def __SteperFrontTurn(self):
        speed = self.Speed
        
        self.__SteperWriteData([1,1,0,0])
        pyb.delay(speed)

        self.__SteperWriteData([0,1,1,0])
        pyb.delay(speed)

        self.__SteperWriteData([0,0,1,1])
        pyb.delay(speed)

        self.__SteperWriteData([1,0,0,1])   
        pyb.delay(speed)
        
    def __SteperBackTurn(self):
        speed = self.Speed
        
        self.__SteperWriteData([1,1,0,0])
        pyb.delay(speed)
        
        self.__SteperWriteData([1,0,0,1])   
        pyb.delay(speed)

        self.__SteperWriteData([0,0,1,1])
        pyb.delay(speed)

        self.__SteperWriteData([0,1,1,0])
        pyb.delay(speed)


    def __SteperStop(self):
        self.__SteperWriteData([0,0,0,0])
        
    def steperRun(self,angle):
        val=ANGLE_PER_ROUND*abs(angle)
        if(angle>0):
            for i in range(0,val):
                self.__SteperFrontTurn()
        else:
            for i in range(0,val):
                self.__SteperBackTurn()
        angle = 0
        self.__SteperStop()