import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


GPIO.setup(4,GPIO.OUT)

# #设置GPIO2为高电平
# GPIO.output(4,GPIO.HIGH)
# #设置GPIO2为低电平
# GPIO.output(4,GPIO.LOW)

continue_time = input("continue time(s):1 or 6")
GPIO.output(4,GPIO.HIGH)
time.sleep((int)(continue_time))
GPIO.output(4,GPIO.LOW)
print("ok")



