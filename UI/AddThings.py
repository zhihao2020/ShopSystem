# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '添加商品.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(427, 389)
        Form.setMinimumSize(QtCore.QSize(427, 389))
        Form.setMaximumSize(QtCore.QSize(427, 389))
        self.add_thing = QtWidgets.QPushButton(Form)
        self.add_thing.setGeometry(QtCore.QRect(260, 330, 93, 28))
        self.add_thing.setObjectName("add_thing")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 60, 325, 250))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.beizhu = QtWidgets.QTextEdit(self.layoutWidget)
        self.beizhu.setObjectName("beizhu")
        self.gridLayout.addWidget(self.beizhu, 4, 2, 1, 1)
        self.add_thing_price = QtWidgets.QLineEdit(self.layoutWidget)
        self.add_thing_price.setObjectName("add_thing_price")
        self.gridLayout.addWidget(self.add_thing_price, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.add_thing_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.add_thing_name.setObjectName("add_thing_name")
        self.gridLayout.addWidget(self.add_thing_name, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "添加商品"))
        self.add_thing.setText(_translate("Form", "添加"))
        self.label_2.setText(_translate("Form", "商品价格"))
        self.label_3.setText(_translate("Form", "简介"))
        self.label.setText(_translate("Form", "商品名称"))

