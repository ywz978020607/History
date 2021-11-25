import time
import win32api,win32con
#
# p_w,p_h = 100,200 #width，height坐标
# delta_time=31

#模拟鼠标点击
def mouse_click(x, y): #[w,h]
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def task1(p_w,p_h,delta_time):
    while 1:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        mouse_click(p_w,p_h)
        time.sleep(delta_time)
        mouse_click(p_w, p_h)
        time.sleep(5) #等待下一次

if __name__=="__main__":
    p_w = int(input("input width coordinate(int):"))
    p_h = int(input("input height coordinate(int):"))
    delta_time = int(input("input delta_time(int):"))

    task1(p_w,p_h,delta_time)

