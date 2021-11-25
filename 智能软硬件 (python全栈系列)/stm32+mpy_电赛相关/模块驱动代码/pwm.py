from pyb import Timer

pwm_pin1 = Pin('PA5',Pin.OUT)
pwm_tim1 = Timer(2)  #not start

ch=self.pwm_tim1.channel(1,Timer.PWM,pin=self.pwm_pin1)
ch.pulse_width_percent(50) #占空比


#停止
pwm_tim1.deinit()