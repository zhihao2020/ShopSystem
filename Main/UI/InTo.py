# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '登录界面.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(503, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        widget.setMinimumSize(QtCore.QSize(503, 350))
        widget.setMaximumSize(QtCore.QSize(503, 350))
        self.InTo = QtWidgets.QPushButton(widget)
        self.InTo.setGeometry(QtCore.QRect(110, 250, 93, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InTo.sizePolicy().hasHeightForWidth())
        self.InTo.setSizePolicy(sizePolicy)
        self.InTo.setObjectName("InTo")
        self.verticalLayoutWidget = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 120, 81, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labe = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labe.setObjectName("labe")
        self.verticalLayout.addWidget(self.labe)
        self.label2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label2.setObjectName("label2")
        self.verticalLayout.addWidget(self.label2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(230, 120, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.name.setObjectName("name")
        self.verticalLayout_2.addWidget(self.name)
        self.Password = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password.setObjectName("Password")
        self.verticalLayout_2.addWidget(self.Password)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(150, 50, 201, 61))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(29)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)
        widget.setTabOrder(self.name, self.Password)
        widget.setTabOrder(self.Password, self.InTo)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "登录"))
        self.InTo.setText(_translate("widget", "登录"))
        self.labe.setText(_translate("widget", "Name"))
        self.label2.setText(_translate("widget", "PassWord"))
        self.label.setText(_translate("widget", "欢迎使用"))

