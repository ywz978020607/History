from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox, QTextEdit, QVBoxLayout
import sys
from PyQt5.QtCore import QTimer
import sys
import os
import requests
import json
import datetime


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
        self.bt2.clicked.connect(self.click2)
        self.bt3.clicked.connect(self.click3)
        self.bt4.clicked.connect(self.click4)
        self.bt5.clicked.connect(self.click5)


    def click1(self):
        message1 = self.message1.text()
        message2 = self.message2.text()
        message3 = self.message3.text()
        #username+123
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example1()
    ex.show()
    sys.exit(app.exec_())