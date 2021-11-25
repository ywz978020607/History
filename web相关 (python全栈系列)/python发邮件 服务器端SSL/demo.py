#第一种 文字版 群发

from smtplib import SMTP,SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
def send():
    # 请自行修改下面的邮件发送者和接收者
    sender = '978020607@qq.com'  #发送者的邮箱地址
    receivers = ['85xxxx00@qq.com']  #接收者的邮箱地址
    message = MIMEText('Alert:您的车辆有风险', _subtype='plain', _charset='utf-8')
    message['From'] = Header('TestSystem', 'utf-8')  #邮件的发送者
    message['To'] = Header('Hello', 'utf-8')   #邮件的接收者
    message['Subject'] = Header('Alert', 'utf-8') #邮件的标题
    # smtper = SMTP('smtp.qq.com',465)
    smtper = SMTP_SSL("smtp.qq.com", 465)
    # 请自行修改下面的登录口令

    smtper.login(sender, 'wjprnxxxxxxx')  #QQ邮箱smtp的授权码
    smtper.sendmail(sender, receivers, message.as_string())
    print('邮件发送完成!')

########################################################
#第二种 带图片单独发
from smtplib import SMTP,SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
def send2(file_path):
    # 请自行修改下面的邮件发送者和接收者
    sender = '978020607@qq.com'  #发送者的邮箱地址
    receivers = '145xxx434@qq.com'  #接收者的邮箱地址

    subject = "警报"  # 主题
    msg = MIMEMultipart('related')
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
    # msg = MIMEText(content)
    msg.attach(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers

    file = open(file_path, "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    msg.attach(img)

    # smtper = SMTP('smtp.qq.com',465)
    smtper = SMTP_SSL("smtp.qq.com", 465)
    # 请自行修改下面的登录口令

    smtper.login(sender, 'wjprxxxx')  #QQ邮箱smtp的授权码
    smtper.sendmail(sender, receivers, msg.as_string())
    print('邮件发送完成!')