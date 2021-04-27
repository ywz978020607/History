#-*-coding:utf-8-*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import serial
import numpy as np
from myui import Ui_Dialog  #UI布局

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# 创建一个matplotlib图形绘制类
# 只和画布有关
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
########################
#uart
uart = serial.Serial('/dev/ttyS0',9600)


###多线程
class uart_in(QThread):
    uart_in_signal = pyqtSignal(str)  #str类型传参
##    def __init__(self,parent=None):
##        super(uart_in,self).__init__(parent)
##        self.working=True
##
##    def __del__(self):
##        self.working=False
##        self.wait()
    def run(self):
        while 1:
            num = uart.inWaiting()
            if num>0:
                rec = uart.read(num).decode() #str
                self.uart_in_signal.emit(rec)
        
            
        


#主界面类
class MainDialogImgBW(QWidget,Ui_Dialog):
    def __init__(self):
        super(MainDialogImgBW,self).__init__()
        #font
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(30)

        font2=QFont()
        font2.setFamily('微软雅黑')
        font2.setBold(False)
        font2.setPointSize(13)
##        font.setWeight(75)
        self.setFont(font)
        #ui
        self.setupUi(self)
        self.setWindowTitle("2019电子设计大赛")
        self.setMinimumSize(0,0)
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox

##        self.F = MyFigure(width=3, height=2, dpi=100)
##        self.gridlayout.addWidget(self.F,0,1)
        
        """Functions"""

        self.bt1 = QPushButton("button1", self)
        self.bt1.move(20, 100)
        self.bt1.clicked.connect(self.plotother)

        #button2
        self.bt2 = QPushButton("send", self)
        self.bt2.move(20, 180)
        self.bt2.clicked.connect(self.bt2_click)

        #linedit
        self.show1=QLabel('ready',self)
        self.show1.resize(200,100)
        self.show1.move(20,500)
        self.show1.setFont(font2)

        #thread
        self.thread = uart_in()
        self.thread.uart_in_signal.connect(self.get_uart_in)
        self.thread.start()
        
    #########
    #function
    def get_uart_in(self,recv):  #有参数传进来(str)
        self.show1.setText(recv)
        
    def bt2_click(self):
        uart.write('aa'.encode())
        QMessageBox.information(self,'提示','发送成功',QMessageBox.Yes)


    def plotother(self):
        F1 = MyFigure(width=11, height=4, dpi=100)
        F1.fig.suptitle("Figuer_4")
        F1.axes1 = F1.fig.add_subplot(221)
        x = np.arange(0, 50)
        y = np.random.rand(50)
        F1.axes1.hist(y, bins=50)
        F1.axes1.plot(x, y)
        F1.axes1.bar(x, y)
        F1.axes1.set_title("hist")
        F1.axes2 = F1.fig.add_subplot(222)

        ## 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        F1.axes2.plot(x, y)
        F1.axes2.set_title("line")
        # 散点图
        F1.axes3 = F1.fig.add_subplot(223)
        F1.axes3.scatter(np.random.rand(20), np.random.rand(20))
        F1.axes3.set_title("scatter")
        # 折线图
        F1.axes4 = F1.fig.add_subplot(224)
        x = np.arange(0, 5, 0.1)
        F1.axes4.plot(x, np.sin(x), x, np.cos(x))
        F1.axes4.set_title("sincos")
        self.gridlayout.addWidget(F1, 0, 2)  #加入布局

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainDialogImgBW()
    main.show()
    #app.installEventFilter(main)
    sys.exit(app.exec_())
