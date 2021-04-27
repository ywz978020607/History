from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox, QTextEdit, QVBoxLayout
import sys
from PyQt5.QtCore import QTimer
import sys
import os
import requests
import json
import datetime


class Example3(QWidget):
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
        pass

    #############################
    #down
    def click4(self):
        url = "http://127.0.0.1:8000/down/"
        headers = {}#,"Connection":"close"}
        data={'username':self.username}
        receive = requests.get(url,headers = headers,params = data)
        print(receive.text)
        ret = json.loads(receive.text)
        result = ret[self.username]
        show_text = "重量\t\t时间\t\t\t订单号\n"
        for ii in range(len(result)):
            show_text+=str(result[ii][0])+"\t\t"+result[ii][1] +"\t\t"+str(result[ii][2]) +"\n"
        self.textEdit.setPlainText(show_text)


    #print
    def click5(self):
        message1 = self.message1.text()
        if message1 == "":
            QMessageBox.warning(self, "提示", "请输入订单号")
        else:
            write_content= "当前订单：\t"+str(message1)+"\n"+'-'*50+"\n用户名\t"+self.username+"\n\n重量\t"+str(self.weight)+"\n\n时间\t"+self.last_time
            self.textEdit.setPlainText(write_content)
            f = open("out.txt",'w',encoding='utf-8')
            f.write(write_content)
            f.close()
        # self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\n点击按钮。</font>")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example3()
    ex.show()
    sys.exit(app.exec_())