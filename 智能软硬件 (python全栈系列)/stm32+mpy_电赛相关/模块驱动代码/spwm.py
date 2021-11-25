from pyb import Timer,DAC,Pin

import _thread

class SPWM():
    def __init__(self,freq=100):
        self.pwm_pin = Pin('PA5',Pin.OUT)
        self.pwm_tim = Timer(2)  #not start
        self.flag = 0 
        self.pp = 50 

    def start(self):
        self.pwm()
        self.modulate()
        while 1:
            if self.flag:
                self.flag = 0 
                #计算self.pp  占空比
                #配置pwm占空比
                self.ch.pulse_width_percent(self.pp)


    def pwm(self,enable=True):
        self.pwm_tim = Timer(2,freq=10000)
        self.ch=self.pwm_tim.channel(1,Timer.PWM,pin=self.pwm_pin)
        self.ch.pulse_width_percent(50)
        
    def modulate(self,freq_m=10):
        self.m_tim = Timer(5,freq=freq_m)
        self.m_tim.callback(lambda t: self.change())
    
    def change(self):
        self.flag = 1