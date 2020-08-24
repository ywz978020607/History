# main.py -- put your code here!
from pyb import Pin
from stepermotor import SteperMotor

Pin_All=[Pin(p,Pin.OUT_PP) for p in ['X1','X2','X3','X4']]

if __name__=='__main__':
    #转速(ms) 数值越大转速越慢 最小值1.8ms
    sm = SteperMotor(pin = Pin_All,speed=2)
    sm.steperRun(-360)
    

