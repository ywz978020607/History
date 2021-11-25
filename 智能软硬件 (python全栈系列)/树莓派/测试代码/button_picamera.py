import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep

GPIO.setmode(GPIO.BCM)
pin_button = 26 
pin_servo1 = 19
pin_fan1   = 13 
pin_servo2 = 21
pin_fan2   = 20 
pin_servo3 = 8
pin_fan3   = 7 
pin_servo4 = 27
pin_fan4   = 17 
button = 26 

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_servo1, GPIO.OUT)
GPIO.setup(pin_fan1,GPIO.OUT)
GPIO.output(pin_fan1,GPIO.LOW)

GPIO.setup(pin_servo2, GPIO.OUT)
GPIO.setup(pin_fan2,GPIO.OUT)
GPIO.output(pin_fan2,GPIO.LOW)

GPIO.setup(pin_servo3, GPIO.OUT)
GPIO.setup(pin_fan3,GPIO.OUT)
GPIO.output(pin_fan3,GPIO.LOW)

GPIO.setup(pin_servo4, GPIO.OUT)
GPIO.setup(pin_fan4,GPIO.OUT)
GPIO.output(pin_fan4,GPIO.LOW)

dutybefore = 2 #关门的角度
dutyafter  = 7 #开门的角度
servo1 = GPIO.PWM(pin_servo1,50)
servo1_state = 0
servo1.start(0)
servo1.start(dutybefore)
sleep(0.5)
servo1.ChangeDutyCycle(0)

servo2 = GPIO.PWM(pin_servo2,50)
servo2_state = 0
servo2.start(0)
servo2.start(dutybefore)
sleep(0.5)
servo2.ChangeDutyCycle(0)

servo3 = GPIO.PWM(pin_servo3,50)
servo3_state = 0
servo3.start(0)
servo3.start(dutybefore)
sleep(0.5)
servo3.ChangeDutyCycle(0)

servo4 = GPIO.PWM(pin_servo4,50)
servo4_state = 0
servo4.start(0)
servo4.start(dutybefore)
sleep(0.5)
servo4.ChangeDutyCycle(0)


camera = PiCamera()
camera.rotation = 180 
camera.resolution = (1080,1920)  #更改为竖屏分辨率（需要先更改树莓派系统文件让它变为竖屏模式）
# camera.resolution = (3280,2464) #使用最高像素拍摄，但速度会变得很慢
camera.framerate = 30
camera.start_preview(fullscreen = True)
count = 1

def event_callback(pin_button):
    global count
    GPIO.remove_event_detect(pin_button)
    data = time.strftime("%H%M%S_%Y-%b-%d")
    camera.capture('/home/pi/Desktop/image-%s.jpg' %data)

    camera.brightness = 0 #制造拍照特效
    sleep(0.3)
    camera.brightness = 50
    camera.annotate_text = "Capture Sucess"
    sleep(1)

    if count == 1:
        GPIO.output(pin_fan1,GPIO.HIGH)
        servo1.ChangeDutyCycle(dutyafter)
        sleep(0.5) 
        servo1.ChangeDutyCycle(0) #舵机去抖动
        count += 1

    if count == 2:
        GPIO.output(pin_fan1,GPIO.LOW)  #关闭上一个门和舵机
        servo1.ChangeDutyCycle(dutybefore)
        sleep(0.5) 
        servo1.ChangeDutyCycle(0) #舵机去抖动

        GPIO.output(pin_fan2,GPIO.HIGH)
        servo2.ChangeDutyCycle(dutyafter)
        sleep(0.5) 
        servo2.ChangeDutyCycle(0) #舵机去抖动
        count += 1

    if count == 3:
        GPIO.output(pin_fan2,GPIO.LOW)  #关闭上一个门和舵机
        servo2.ChangeDutyCycle(dutybefore)
        sleep(0.5) 
        servo2.ChangeDutyCycle(0) #舵机去抖动

        GPIO.output(pin_fan3,GPIO.HIGH)
        servo3.ChangeDutyCycle(dutyafter)
        sleep(0.5) 
        servo3.ChangeDutyCycle(0) #舵机去抖动
        count += 1

    if count == 4:
        GPIO.output(pin_fan3,GPIO.LOW)  #关闭上一个门和舵机
        servo3.ChangeDutyCycle(dutybefore)
        sleep(0.5) 
        servo3.ChangeDutyCycle(0) #舵机去抖动

        GPIO.output(pin_fan4,GPIO.HIGH)
        servo4.ChangeDutyCycle(dutyafter)
        sleep(0.5) 
        servo4.ChangeDutyCycle(0) #舵机去抖动
        count += 1
    
    if count == 5:
        GPIO.output(pin_fan4,GPIO.LOW)  #关闭上一个门和舵机
        servo4.ChangeDutyCycle(dutybefore)
        sleep(0.5) 
        servo4.ChangeDutyCycle(0) #舵机去抖动

        camera.annotate_text = "THE END"
        count = 0
        camera.brightness = 0 #制造黑屏效果提示拍照结束
        time.sleep(3)
        camera.brightness = 50
        count = 1

    GPIO.add_event_detect(pin_button, GPIO.RISING, callback=event_callback, bouncetime=1000) #去除按钮抖动

GPIO.add_event_detect(pin_button, GPIO.RISING, callback=event_callback, bouncetime=1000) #去除按钮抖动

try:
    while True:   #r让程序保持循环运行状态
        pass
except KeyboardInterrupt: #如果按下CTRL+C终止程序将会执行清除操作
    GPIO.remove_event_detect(pin_button)
    GPIO.cleanup()
    camera.stop_preview()