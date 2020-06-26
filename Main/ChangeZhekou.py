from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtCore import pyqtSignal
from UI.zhekou import Ui_Form
class ChangePrice(QWidget,Ui_Form):
    Signal_TwoParameter = pyqtSignal(list)
    def __init__(self,name,price,row):
        super(ChangePrice,self).__init__()
        self.setupUi(self)
        self.label_3.setText(name)
        self.price = price
        self.pushButton.clicked.connect(self.emitSingal)
        self.row = row

    def emitSingal(self):
        if float(self.lineEdit.text()) > 1:
            print(QMessageBox.critical(self, "警告", "折扣应该小于1", QMessageBox.Yes))
        elif float(self.lineEdit.text()) < 0:
            print(QMessageBox.critical(self, "警告", "折扣应该大于0", QMessageBox.Yes))
        else:
            price = str(float(self.price) * float(self.lineEdit.text()))[0:5]
            lis =[price,self.row]
            self.Signal_TwoParameter[list].emit(lis)
            self.close()
