from match import *
import random,time,win32api,win32con
from capture import *

vote_template = "a.png"
sele_template = ["0.png","1.png","2.png","3.png"]
check_template = "check.png" #确认答题
vote_now = "vote_now.png"

def check(fig1,fig2):
    temp = template_matching(fig1,fig2,0.999999)
    if temp[0] != {}: #不为空
        print("check.")
        res = temp[0][list(temp[0].keys())[0]]  #(41,108)
        #点击
        win32api.SetCursorPos([res[0],res[1]])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)       
        return True
    return False

#鼠标定位到(30,50)
#win32api.SetCursorPos([30,150])
#执行左单键击，若需要双击则延时几毫秒再点击一次即可
#win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def fresh_now():
    window_capture("vote_now.png")
    print("save fig.")

# 整体流程
def task():
    # 检测题目
    fresh_now() # 更新图片
    vote_template_now = vote_template
    flag = check(vote_template,vote_now)
    if flag:
        print("wait")
        time.sleep(2)
        sele = random.randint(0,4) #ABCD
        print(sele)
        # 更新图片
        fresh_now()
        flag = False
        while not flag:
            flag = check(sele_template[sele],vote_now)
            time.sleep(1)

        fresh_now()
        # 点击确认
        flag = False
        while not flag:
            flag = check(check_template,vote_now)
            time.sleep(1)
        print("once ok.")


if __name__ == "__main__":
    while 1:
        try:
            task()
        except:
            print("error")

        time.sleep(1)

