# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '添加用户信息.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 212)
        Form.setMinimumSize(QtCore.QSize(300, 212))
        Form.setMaximumSize(QtCore.QSize(300, 212))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.add_thing_name = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.add_thing_name.setFont(font)
        self.add_thing_name.setObjectName("add_thing_name")
        self.gridLayout.addWidget(self.add_thing_name, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 3, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setFamily("SimSun-ExtB")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.add_thing = QtWidgets.QPushButton(Form)
        self.add_thing.setObjectName("add_thing")
        self.verticalLayout.addWidget(self.add_thing)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.add_thing_name, self.spinBox)
        Form.setTabOrder(self.spinBox, self.lineEdit)
        Form.setTabOrder(self.lineEdit, self.add_thing)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "添加用户信息"))
        self.label_3.setText(_translate("Form", "年龄"))
        self.label.setText(_translate("Form", "用户姓名"))
        self.label_4.setText(_translate("Form", "电话"))
        self.dateEdit.setDisplayFormat(_translate("Form", "yyyy/MM/dd"))
        self.label_2.setText(_translate("Form", "生日"))
        self.add_thing.setText(_translate("Form", "添加"))
