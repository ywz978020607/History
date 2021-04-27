# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'testplot2pyqt5.ui'
# Created by: PyQt5 UI code generator 5.10
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 600) # 总大小

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(200, 10, 812, 580)) # 对话框大小
        self.widget.setObjectName("widget")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 789, 560)) # widge大小
        self.groupBox.setObjectName("groupBox")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox_Matplotlib的图形显示："))
