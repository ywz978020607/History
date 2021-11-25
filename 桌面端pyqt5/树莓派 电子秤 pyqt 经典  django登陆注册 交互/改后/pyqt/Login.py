from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu, QLabel, QLineEdit, QMessageBox, QTextEdit, \
    QVBoxLayout
import datetime
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox
import sys
import os
import json
import time
import requests
from PyQt5.QtCore import Qt
# from Main_no_hx711 import  *

import RPi.GPIO as GPIO
from hx711 import HX711


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500,500)
        self.setWindowTitle('智能称重')
       # self.count = 10 #默认10s

        self.text1 = QLabel("Username", self)
        self.text1.move(30, 20)
        self.text2 = QLabel("Password", self)
        self.text2.move(30, 100)
        # create textbox
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(100, 20)
        self.textbox1.resize(280, 40)
        # create textbox
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(100, 100)
        self.textbox2.resize(280, 40)
        self.textbox2.setContextMenuPolicy(Qt.NoContextMenu)#这个语句设置QLineEdit对象的上下文菜单的策略。复制，粘贴，。。。，是否可用
        self.textbox2.setPlaceholderText("密码不超15位，只能有数字和字母，必须以字母开头")#只要行编辑为空，设置此属性将使行编辑显示为灰色的占位符文本。默认情况下，此属性包含一个空字符串。这是非常好的使用方法，可以在用户输入密码前看到一些小提示信息，但是又不影响使用，非常棒这个方法。
        self.textbox2.setEchoMode(QLineEdit.Password)#这条语句设置了如何限定输入框中显示其包含信息的方式，这里设置的是：密码方式，即输入的时候呈现出原点出来。

        self.bt1 = QPushButton("登陆", self)
        self.bt1.resize(100, 100)
        self.bt1.move(100, 300)
        self.bt2 = QPushButton("注册", self)
        self.bt2.resize(100, 100)
        self.bt2.move(300, 300)

        ############################################################################################
        self.bt1.clicked.connect(self.click1)
        self.bt2.clicked.connect(self.click2)
        # self.show()

    def click1(self):
        url = "http://127.0.0.1:8000/login/"
        headers = {}#,"Connection":"close"}

        data={'username': self.textbox1.text(),"password": self.textbox2.text()}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        if receive.text == 'yes':
            #1打开新窗口
            ex1.get_username(self.textbox1.text())
            ex1.show()
            #2关闭本窗口
            self.close()
        else:
            reply = QMessageBox.warning(self, "警告", "账户或密码错误，请重新输入！")

    def click2(self):
        url = "http://127.0.0.1:8000/register/"
        headers = {}#,"Connection":"close"}

        data={'username': self.textbox1.text(),"password": self.textbox2.text()}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        if receive.text != "ok":
            reply = QMessageBox.warning(self, "提示", "已注册")
        else:
            reply = QMessageBox.warning(self, "提示",receive.text)


class Example1(QWidget):
    #传入username
    def get_username(self,name):
        self.username = name
        print(name)


    def __init__(self):
        super().__init__()
        self.initUI()
        self.username = "ywz"
        self.weight = 0
        self.base_weight = 0 #去皮
        self.last_time = ''

    def initUI(self):
        self.resize(700,700)
        self.setWindowTitle('智能称重')
       # self.count = 10 #默认10s
        self.text1 = QLabel("订单号", self)
        self.text1.move(150, 100)
        self.message1 = QLineEdit("", self)
        self.message1.move(200, 100)

        self.text2 = QLabel("规格", self)
        self.text2.move(150, 200)
        self.message2 = QLineEdit("", self)
        self.message2.move(200, 200)

        self.text3 = QLabel("名称", self)
        self.text3.move(150, 300)
        self.message3 = QLineEdit("", self)
        self.message3.move(200, 300)

        self.bt1 = QPushButton("下一步", self)
        self.bt1.resize(100, 100)
        self.bt1.move(400, 200)
        ####
        self.bt1.clicked.connect(self.click1)


    def click1(self):
        m1 = str(self.message1.text())
        m2 = str(self.message2.text())
        m3 = str(self.message3.text())

        #username+123
        #1打开新窗口
        ex2.get_username(self.username,m1,m2,m3)
        ex2.show()
        #2关闭本窗口
        self.close()

class Example2(QWidget):
    #传入username
    def get_username(self, name, m1,m2,m3):
        self.username = name
        self.m1 = str(m1)
        self.m2 = str(m2)
        self.m3 = str(m3)
        print(self.m1)
        print(self.m2)
        print(self.m3)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.username = "ywz"
        self.m1 = "m1"
        self.m2 = "m2"
        self.m3 = "m3"
        self.weight = 0
        self.base_weight = 0 #去皮
        self.last_time = ''

        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(1)
        self.hx.reset()

    def initUI(self):
        self.resize(700,300)
        self.setWindowTitle('智能称重')
       # self.count = 10 #默认10s
        self.text1 = QLabel("重量/kg", self)
        self.text1.move(200, 50)
        self.text2 = QLabel("0", self)
        self.text2.move(300, 50)

        self.bt1 = QPushButton("去皮", self)
        self.bt1.resize(100, 100)
        self.bt1.move(100, 200)
        self.bt2 = QPushButton("称重", self)
        self.bt2.resize(100, 100)
        self.bt2.move(250, 200)
        self.bt3 = QPushButton("上传", self)
        self.bt3.resize(100, 100)
        self.bt3.move(400, 200)
        self.bt4 = QPushButton("下一步", self)
        self.bt4.resize(100, 100)
        self.bt4.move(550, 200)
        ####
        self.bt1.clicked.connect(self.click1)
        self.bt2.clicked.connect(self.click2)
        self.bt3.clicked.connect(self.click3)
        self.bt4.clicked.connect(self.click4)

    #去皮
    def click1(self):
        # self.base_weight = 0
        self.hx.tare()  # 去皮
        QMessageBox.warning(self, "提示", "去皮完成")
    #称重
    def click2(self):
        # self.weight = 1.0-self.base_weight
        self.weight = (float)(self.hx.get_weight(5) / 92000)
        # self.weight = str(self.weight)
        self.weight = format(self.weight, '.2f')
        self.text2.setText(str(self.weight))
        self.last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        QMessageBox.warning(self, "提示", "称重完成")

    #up
    def click3(self):
        url = "http://127.0.0.1:8000/up/"
        headers = {}#,"Connection":"close"}
        data={'username':self.username,"weight":self.weight,"time":self.last_time,"message1":self.m1,
              'message2':self.m2,'message3':self.m3}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        QMessageBox.warning(self, "提示", receive.text)

    def click4(self):
        # 1打开新窗口
        ex3.get_username(self.username,self.weight,self.last_time,self.m1,self.m2,self.m3)
        ex3.show()
        # 2关闭本窗口
        self.close()


class Example3(QWidget):
    #传入username
    def get_username(self,name,weight,last_time, m1,m2,m3):
        self.username = name
        self.weight = weight
        self.last_time = last_time
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

        print(name)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.username = "ywz"
        self.weight = 0
        self.last_time = '未上传'

    def initUI(self):
        self.resize(700,600)
        self.setWindowTitle('智能称重')
       # self.count = 10 #默认10s
        self.bt3 = QPushButton("下一单", self)
        self.bt3.resize(100, 100)
        self.bt3.move(150, 50)
        self.bt4 = QPushButton("查询历史", self)
        self.bt4.resize(100, 100)
        self.bt4.move(300, 50)
        self.bt5 = QPushButton("打印标签", self)
        self.bt5.resize(100, 100)
        self.bt5.move(450, 50)

        self.textEdit = QTextEdit(self)
        self.textEdit.resize(600, 400)
        self.textEdit.move(50, 170)

        # self.textEdit.show()

        ############################################################################################
        self.bt3.clicked.connect(self.click3)
        self.bt4.clicked.connect(self.click4)
        self.bt5.clicked.connect(self.click5)

        # self.show()


    #next
    def click3(self):
        # 1打开新窗口
        ex1.get_username(self.username)
        ex1.show()
        # 2关闭本窗口
        self.close()

    #############################
    #down
    def click4(self):
        url = "http://127.0.0.1:8000/down/"
        headers = {}#,"Connection":"close"}
        data={'username':self.username}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        ret = json.loads(receive.text)
        result = ret[self.username]  #数组
        show_text=''
        for ii in range(len(result)):

            show_text+="重量\t" + str(result[ii][0])+"\n"+"时间\t" + str(result[ii][1])+"\n"+"订单号\t" + str(result[ii][2])+"\n"+ \
                       "规格\t" + str(result[ii][3]) + "\n" +"名称\t" + str(result[ii][4])+"\n"
            show_text +='-'*30
            show_text+='\n'

        self.textEdit.setPlainText(show_text)


    #print
    def click5(self):
        write_content= '-'*50+"\n当前订单：\t"+str(self.m1)+"\n"\
                       +"规格：\t"+str(self.m2)+"\n"+"名称：\t"+str(self.m3)+"\n"+"重量：\t"+str(self.weight)+"\n"\
                       +"\n时间\t"+self.last_time+"\n\n"#重量\t"+str(self.weight)+"\n\n时间\t"+self.last_time
        self.textEdit.setPlainText(write_content)
        f = open("out.txt",'w',encoding='utf-8')
        f.write(write_content)
        f.close()
    # self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\n点击按钮。</font>")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex0 = Login()
    ex1 = Example1()
    ex2 = Example2()
    ex3 = Example3()

    ex0.show() #只先显示登陆界面
    sys.exit(app.exec_())


