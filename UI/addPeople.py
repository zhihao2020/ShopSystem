# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '添加用户充值.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setMaximumSize(QtCore.QSize(400, 300))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_2.setMaximum(999999999.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 7, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.add_thing_name = QtWidgets.QLineEdit(Form)
        self.add_thing_name.setObjectName("add_thing_name")
        self.gridLayout.addWidget(self.add_thing_name, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 2, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 4, 2, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setMaximum(99999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 5, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 6, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.add_thing = QtWidgets.QPushButton(Form)
        self.add_thing.setObjectName("add_thing")
        self.verticalLayout.addWidget(self.add_thing)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.add_thing_name, self.spinBox)
        Form.setTabOrder(self.spinBox, self.lineEdit)
        Form.setTabOrder(self.lineEdit, self.comboBox)
        Form.setTabOrder(self.comboBox, self.spinBox_2)
        Form.setTabOrder(self.spinBox_2, self.doubleSpinBox_2)
        Form.setTabOrder(self.doubleSpinBox_2, self.add_thing)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "充值"))
        self.label_2.setText(_translate("Form", "手法名称"))
        self.label.setText(_translate("Form", "用户姓名"))
        self.label_5.setText(_translate("Form", "商品余额"))
        self.label_3.setText(_translate("Form", "年龄"))
        self.label_4.setText(_translate("Form", "电话"))
        self.label_6.setText(_translate("Form", "次数"))
        self.add_thing.setText(_translate("Form", "添加"))
