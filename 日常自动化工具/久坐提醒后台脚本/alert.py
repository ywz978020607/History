import time,win32api,win32con

Period_Time = 50 #min
while 1:
    time.sleep(Period_Time)
    button = win32api.MessageBox(0, "为了健康奋斗五十年，快去休息一下~", "提醒喝水运动小助手", win32con.MB_OKCANCEL)
    if button == 1:
        continue
    else:
        break

##pyinstaller -F -w alert.py