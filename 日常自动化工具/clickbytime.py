import pyautogui as pg
import datetime
import time

target_time = '03:13'

while 1:
    now = datetime.datetime.now()
    now_time = now.strftime("%H:%M")
    if now_time == target_time:
        pg.moveTo(871, 666, 0.1)
        pg.click()
        break
    time.sleep(10)

