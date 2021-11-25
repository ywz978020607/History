from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QTimer
import sys
import os
import requests
import json
import datetime


class Example(QWidget):
    # #传入username
    # def get_username(self,name):
    #     self.username = name
    #     print(name)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600,300)
        self.setWindowTitle('智能称重')
       # self.count = 10 #默认10s

        self.text1 = QLabel("重量/kg", self)
        self.text1.move(200, 50)
        self.text2 = QLabel("0", self)
        self.text2.move(300, 50)
        # self.text2.setText(str(self.weight))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())