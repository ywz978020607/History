from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu ,QLabel ,QLineEdit,QMessageBox, QTextEdit, QVBoxLayout
import sys
from PyQt5.QtCore import QTimer
import sys
import os
import requests
import json
import datetime


class Example(QWidget):
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

        self.text1 = QLabel("重量/kg", self)
        self.text1.move(200, 50)
        self.text2 = QLabel("0", self)
        self.text2.move(300, 50)

        self.text3 = QLabel("订单号", self)
        self.text3.move(150, 100)
        self.message1 = QLineEdit("",self)
        self.message1.move(200,100)

        self.bt1 = QPushButton("去皮",self)
        self.bt1.resize(100, 100)
        self.bt1.move(150, 200)
        self.bt2 = QPushButton("称重", self)
        self.bt2.resize(100, 100)
        self.bt2.move(300, 200)
        self.bt3 = QPushButton("上传", self)
        self.bt3.resize(100, 100)
        self.bt3.move(450, 200)
        self.bt4 = QPushButton("查询历史", self)
        self.bt4.resize(100, 100)
        self.bt4.move(300, 600)
        self.bt5 = QPushButton("打印标签", self)
        self.bt5.resize(100, 100)
        self.bt5.move(450, 50)

        self.textEdit = QTextEdit(self)
        self.textEdit.resize(500, 300)
        self.textEdit.move(100, 310)

        # self.textEdit.show()

        ############################################################################################
        self.bt1.clicked.connect(self.click1)
        self.bt2.clicked.connect(self.click2)
        self.bt3.clicked.connect(self.click3)
        self.bt4.clicked.connect(self.click4)
        self.bt5.clicked.connect(self.click5)

        # self.show()

    #去皮
    def click1(self):
        self.base_weight = 0
        QMessageBox.warning(self, "提示", "去皮完成")
    #称重
    def click2(self):
        self.weight = 1.0-self.base_weight
        self.text2.setText(str(self.weight))
        self.last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        QMessageBox.warning(self, "提示", "称重完成")

    #up
    def click3(self):
        message1 = self.message1.text()
        if message1=="":
            QMessageBox.warning(self, "提示", "请输入订单号")
        else:
            url = "http://127.0.0.1:8000/up/"
            headers = {}#,"Connection":"close"}
            data={'username':self.username,"weight":self.weight,"time":self.last_time,"message1":message1}
            receive = requests.get(url,headers = headers,params = data)
            print(receive.text)
            QMessageBox.warning(self, "提示", receive.text)

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
    ex = Example()
    ex.show()
    sys.exit(app.exec_())