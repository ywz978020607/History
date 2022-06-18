        # #2 查询数据库，判定是否有匹配
        # ms = MSSQL()
        # result = ms.Login_result(account, password)
        # if(len(result) > 0):
        #     #1打开新窗口
        #     Ui_Main.show()
        #     #2关闭本窗口
        #     self.close()
        # else:
        #     reply = QMessageBox.warning(self,"警告","账户或密码错误，请重新输入！")


from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox
from PyQt5.QtCore import QTimer
import sys
import os
import json
import time
import requests
from PyQt5.QtCore import Qt
from Main import  *


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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex0 = Login()
    ex1 = Example()
    ex0.show() #只先显示登陆界面
    sys.exit(app.exec_())


