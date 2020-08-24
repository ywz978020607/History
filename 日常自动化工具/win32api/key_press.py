import win32api
import win32con
import time

time.sleep(5)

win32api.keybd_event(0x41,0,0,0)     # enter
win32api.keybd_event(0x41,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键

print("ok")