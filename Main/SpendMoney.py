from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtCore import pyqtSignal
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 169)
        Form.setMaximumSize(QtCore.QSize(400, 169))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setMaximum(9999999)
        self.doubleSpinBox.setMinimum(-9999999)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "消费金额"))
        self.label.setText(_translate("Form", "姓名"))
        self.label_2.setText(_translate("Form", "电话"))
        self.label_3.setText(_translate("Form", "消费金额"))
        self.pushButton.setText(_translate("Form", "确定"))

class SpendWindow(QtWidgets.QWidget,Ui_Form):
    Signal_TwoParameter = pyqtSignal(list)
    def __init__(self):
        super(SpendWindow,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.emitSignal)

    def emitSignal(self):
        if self.lineEdit.text():
            a = self.lineEdit.text().strip()
        elif self.lineEdit_2.text():
            a = self.lineEdit_2.text().strip()
        else:
            a = None
        money = self.doubleSpinBox.value()
        lis = [a,money]

        self.Signal_TwoParameter[list].emit(lis)
        self.lineEdit.setText(" ")
        self.doubleSpinBox.setValue(0)