#跑自动化脚本时防电脑睡眠 特别是新版macos总是自动睡眠
import pyautogui as pg
import time

last_x,last_y = 0,0
while 1:
    x,y = pg.position()
    if x==last_x and y==last_y:
        #太久不动了
        pg.moveTo(400,400,0.1)
        pg.moveTo(500,500,0.1)

    last_x = x
    last_y = y

    time.sleep(50)