# python this.py xxx@qq.com
# 防止休眠 & 检测发送邮件通知
#跑自动化脚本时防电脑睡眠 特别是新版macos总是自动睡眠
import pyautogui as pg
import time
import os,sys
import time
from smtplib import SMTP, SMTP_SSL # pip install PyEmail
from email.header import Header
from email.mime.text import MIMEText


def alert(receiver, alert_context="服务器脚本提醒-"):
	# 请自行修改下面的邮件发送者和接收者
	sender = '978020607@qq.com'  # 发送者的邮箱地址
	receivers = [receiver]  # 接收者的邮箱地址
	message = MIMEText('Alert:'+str(alert_context), _subtype='plain', _charset='utf-8')
	message['From'] = Header('TestSystem', 'utf-8')  # 邮件的发送者
	message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
	message['Subject'] = Header(alert_context, 'utf-8')  # 邮件的标题
	# smtper = SMTP('smtp.qq.com',465)
	smtper = SMTP_SSL("smtp.qq.com", 465)
	# 请自行修改下面的登录口令

	smtper.login(sender, 'jdcyrnwpwbiwbbee')  # QQ邮箱smtp的授权码
	smtper.sendmail(sender, receivers, message.as_string())
	print('邮件发送完成!')


def check_color(pos_x = 564,pos_y = 877):
    # print("color:{}".format((pg.screenshot().getpixel((190,99)))))
    if max(pg.screenshot().getpixel((pos_x,pos_y))) > 180:
        # 白色
        return True
    else:
        return False

if __name__ == "__main__":
    pg.screenshot(r'test.png')
    # print(pg.size()) #1920, 1080
    # print(max(pg.screenshot().getpixel((190,99)))) #(11, 9, 14) -- 14
    alert(str(sys.argv[1]),"脚本运行")
    last_x,last_y = 10,10
    pg.moveTo(last_x,last_y,0.1)
    while 1:
        if check_color():
            alert(str(sys.argv[1]),"脚本通知")
        x,y = pg.position()
        if x==last_x and y==last_y:
            #太久不动了
            pg.moveTo(400,400,0.1)
            pg.moveTo(500,500,0.1)

        last_x = x
        last_y = y

        time.sleep(60)


