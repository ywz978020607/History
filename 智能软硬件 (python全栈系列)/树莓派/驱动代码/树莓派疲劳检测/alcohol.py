import RPi.GPIO as GPIO
import time
 
pin_alcohol=13

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_alcohol, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.OUT)#fengmingqi

 
try:
    while True:
        status = GPIO.input(pin_alcohol)
        if status == True:
            print('没有检测到xiyan')
            GPIO.output(21,GPIO.HIGH)
            time.sleep(1)
        else:
            print('检测到有xiyan')
            GPIO.output(21,GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(21,GPIO.HIGH)
            time.sleep(0.05)
            
        time.sleep(1)
except KeyboradInterrupt:
    GPIO.cleanup()