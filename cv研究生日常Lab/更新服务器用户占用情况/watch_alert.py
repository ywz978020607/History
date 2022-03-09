# python watch_alert.py 4.5 ywzsunny@buaa.edu.cn all  # 阈值/G 邮箱 监控显卡
# python watch_alert.py 8 ywzsunny@buaa.edu.cn all xxxx # 阈值/G 邮箱 监控显卡 自定义额外通知内容xxxx

# 用法二：
#可嵌入任何脚本结束
# [python xxx(你的脚本) ]   && python /xxxx/watch_alert.py xxxx@qq.com xxxx

import os
import time
# import psutil
import sys
from smtplib import SMTP, SMTP_SSL # pip install PyEmail
from email.header import Header
from email.mime.text import MIMEText


def task1():
    # out_cpu = psutil.cpu_percent(1)
    # out_mem = psutil.virtual_memory().percent

    p = os.popen('nvidia-smi')

    out = p.read()
    all_lines = out.split('\n')
    gpu_data = []

    for ii in range(len(all_lines)):
        if 'Default' in all_lines[ii]:
            gpu_data.append([all_lines[ii-1].split('|')[1].strip().split(' ')[0],all_lines[ii].split('|')[2].strip()])
    
    #deal free
    for ii in range(len(gpu_data)):
        gpu_id = str(gpu_data[ii][0]).strip()
        catstr = "".join(gpu_data[ii][1:]).strip().upper().replace("MIB","") #xxx / xxx
        size_list = catstr.split("/")
        used_size = float(size_list[0].strip())
        all_size = float(size_list[-1].strip())
        free_size = all_size - used_size
        # gpu_data[ii] = free_size

        if free_size >= free_shreshold * 1024:
            #判断&alert
            if watch_gpu == "all" or str(watch_gpu) == str(gpu_id):
                return True
    return False

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

############
if __name__ == "__main__":
    free_shreshold = 8 #G
    if len(sys.argv) > 1:
        if '@' in str(sys.argv[1]):
            # 参数1为邮箱-> 附在脚本后直接通知的用法
            last_append = ""
            if len(sys.argv) > 2:
                last_append = str(sys.argv[2])
            alert(str(sys.argv[1]),"脚本运行结束" + last_append)
            sys.exit() #end
        else:
            #显卡监听模式--normal
            free_shreshold = float(sys.argv[1])
            print("free_shreshold/G:",str(free_shreshold))

    user_email = "ywzsunny@buaa.edu.cn"
    if len(sys.argv) > 2:
        user_email = str(sys.argv[2])
        print("user_email:",user_email)

    watch_gpu = "all"
    if len(sys.argv) > 3:
        watch_gpu = str(sys.argv[3])
        print("watch_gpu:",watch_gpu)

    append_alert_context = ""
    if len(sys.argv) > 4:
        append_alert_context = "\n" + str(sys.argv[4])
        print("append_alert_context:",append_alert_context)

    while 1:
        status = task1()
        if status:
            #延时校验
            time.sleep(30)
            status = task1()
            if status:
                alert(receiver = user_email, alert_context = "显卡已空闲！" + append_alert_context)
                break
        time.sleep(30)
