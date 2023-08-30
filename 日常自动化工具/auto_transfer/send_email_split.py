from smtplib import SMTP, SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

####
# 调用例程
# tfile = 'options_installer.part01.rar'
# send("xxxxx@163.com", "xxx驱动", tfile)

# 可带附件的邮件发送函数
def send(receiver,alert_context, tfile=''):
    # 请自行修改下面的邮件发送者和接收者
    sender = 'xxxxx@qq.com'  # 发送者的邮箱地址
    receivers = [receiver]  # 接收者的邮箱地址
    if tfile:
        message = MIMEMultipart()
    else:
        message = MIMEText('Alert:'+str(alert_context), _subtype='plain', _charset='utf-8')
    message['From'] = sender #Header(sender, 'utf-8')  # 邮件的发送者
    message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
    message['Subject'] = Header(alert_context, 'utf-8')  # 邮件的标题

    if tfile:
        txtfile = MIMEApplication(open(tfile, 'rb').read())
        txtfile.add_header('Content-Disposition','attachment',filename=tfile)
        message.attach(txtfile)

    # smtper = SMTP('smtp.qq.com',465)
    smtper = SMTP_SSL("smtp.qq.com", 465)
    # 请自行修改下面的登录口令

    smtper.login(sender, 'jdxxxxxxxxxx')  # QQ邮箱smtp的授权码
    smtper.sendmail(sender, receivers, message.as_string())
    print('邮件发送完成!')

if __name__ == "__main__":
    folder_path = "output_convert"
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_name_path = folder_path + "/" + file_name
        # if re.findall("part..*.rar", file_name_path):
        if ".txt" in file_name_path:
            send("xxxxx@163.com", "xxxx驱动", file_name_path)
