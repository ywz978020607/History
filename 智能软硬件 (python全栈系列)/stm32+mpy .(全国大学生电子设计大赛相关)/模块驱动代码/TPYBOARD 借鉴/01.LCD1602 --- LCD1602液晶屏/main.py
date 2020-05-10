# main.py -- put your code here!
import pyb
from pyb import Pin
from pyb import delay, udelay,millis
from tpyb_lcd1602 import TPYBoardLcd1602Api
from LCD1602 import TPYBoardGpioLcd1602

lcd = TPYBoardGpioLcd1602(rs_pin=Pin.board.Y10,
              enable_pin=Pin.board.Y9,
              d4_pin=Pin.board.Y5,
              d5_pin=Pin.board.Y6,
              d6_pin=Pin.board.Y7,
              d7_pin=Pin.board.Y8,
              num_lines=2, num_columns=16)
lcd.lcd1602_write_string("Hi,TurnipSmart!\n This TPYBoard!")
delay(5000)
lcd.clear()
lcd.lcd1602_write_string("This  lcd1602!\n Start Work!")
delay(5000)
lcd.clear()
count = 0
while True:
    lcd.move_to(0, 0)
    #%1d 宽度  返回运行当前程序的累计时间，单位是毫秒
    lcd.lcd1602_write_string("%1d" % (millis() // 1000))
    delay(1000)
    count += 1
    print(count)