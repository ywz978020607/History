from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox, QTextEdit, QVBoxLayout
import sys
from PyQt5.QtCore import QTimer
import sys
import os
import requests
import json
import datetime


class Example2(QWidget):
    #传入username
    def get_username(self, name):
        self.username = name
        print(name)

    def get_info(self, message1,message2,message3):
        self.message1 = message1
        self.message2 = message2
        self.message3 = message3
        print(self.message1)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.username = "ywz"
        self.message1 = "m1"
        self.message2 = "m2"
        self.message3 = "m3"
        self.weight = 0
        self.base_weight = 0 #去皮
        self.last_time = ''

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

    #去皮
    def click1(self):
        self.base_weight = 0
        QMessageBox.warning(self, "提示", "去皮完成")
    #称重
    def click2(self):
        self.weight = 1.0-self.base_weight
        self.weight = format(self.weight, '.2f')
        self.text2.setText(str(self.weight))
        self.last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        QMessageBox.warning(self, "提示", "称重完成")

    #up
    def click3(self):
        url = "http://127.0.0.1:8000/up/"
        headers = {}#,"Connection":"close"}
        data={'username':self.username,"weight":self.weight,"time":self.last_time,"message1":self.message1,
              'message2':self.message2,'message3':self.message3}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        QMessageBox.warning(self, "提示", receive.text)

    def click4(self):

        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example2()
    ex.show()
    sys.exit(app.exec_())