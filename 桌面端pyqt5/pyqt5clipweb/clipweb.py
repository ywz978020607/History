import sys
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * #QApplication,QMainWindow
from PyQt5.QtCore import * #QFileInfo, QUrl
from PyQt5.QtWebEngineWidgets import * #QWebEngineView
import json
import os

config_path = "config.json"
icopath = "ico.ico" #支持png等格式
class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()
 
    def createMenu(self):
        self.menu = QtWidgets.QMenu()
        self.showAction1 = QtWidgets.QAction("精简", self, triggered=self.show_window)
        self.showAction2 = QtWidgets.QAction("详细", self, triggered=self.show_full_window)
        self.quitAction = QtWidgets.QAction("保存退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)
 
		# 设置图标
        self.setIcon(QtGui.QIcon(icopath))
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)
 
    def showMsg(self):
        self.showMessage("小工具", "已缩起, 单击/右键调出", self.icon)
 
    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()
        self.ui.setWindowFlags(Qt.SplashScreen | Qt.WindowTransparentForInput)
        self.ui.setWindowOpacity(self.ui.config_dict['opacity']) # 半透明
        self.ui.show()

    def show_full_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()
        self.ui.setWindowFlags(QtCore.Qt.Window)
        self.ui.setWindowOpacity(1.0) # 半透明
        self.ui.show()

    def hid_window(self):
        # 若不是最小化，则最小化
        self.ui.showMinimized()
        self.ui.setWindowFlags(QtCore.Qt.SplashScreen | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.showMsg()

    def quit(self):
        # save
        self.ui.update_location()
        with open(config_path, 'w') as f:
            json.dump(self.ui.config_dict, f)
        QtWidgets.qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            # self.showMessage("xxxx", "点击退出", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                self.show_window()
            else:
                self.hid_window()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config_dict = {
            "geometry": [5, 30, 1355, 730],
            "opacity": 0.7,
            "modify_mode": False,
            "zoom": 0.1
        }
        if os.path.exists(config_path):
            print(config_path)
            with open(config_path, 'r') as f:
                last_config_dict = json.load(f)
                self.config_dict.update(last_config_dict)
                print(self.config_dict)

        self.setWindowTitle('Title')
        if len(self.config_dict.get('geometry', [])) == 4:
            self.setGeometry(self.config_dict.get('geometry', [])[0], self.config_dict.get('geometry', [])[1],self.config_dict.get('geometry', [])[2],self.config_dict.get('geometry', [])[3])
        self.setWindowOpacity(self.config_dict['opacity']) # 半透明

        self.browser=QWebEngineView()
        self.browser.setZoomFactor(self.config_dict['zoom'])
        #加载外部的web界面
        # self.browser.load(QUrl('https://blog.csdn.net/jia666666'))
        self.browser.load(QUrl(QFileInfo("./frontend/index.html").absoluteFilePath()))
        self.setCentralWidget(self.browser)
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowTransparentForInput) #去掉标题栏和任务栏 | #鼠标穿透
        
        self.update_location()



    def update_location(self):
        print("widget.geometry().x() = %d" % self.geometry().x())
        print("widget.geometry().y() = %d" % self.geometry().y())
        print("widget.geometry().width() = %d" % self.geometry().width())
        print("widget.geometry().height() = %d" % self.geometry().height())
        self.config_dict["geometry"] = [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()]

    #     self.bt1 = QPushButton("1111", self)
    #     self.bt1.resize(100, 100)
    #     self.bt1.clicked.connect(self.click1)
    # def click1(self):
    #     print("press")
        



if __name__ == '__main__':
    if 1:
        # 启动server
        app = QApplication(sys.argv)
        main_ = MainWindow()
        # main_.showMinimized()
        main_.show()
        tray = TrayIcon(main_)
        tray.show()
        sys.exit(app.exec_())
    else:
        app=QApplication(sys.argv)
        win=MainWindow()
        win.show()
        app.exit(app.exec_())