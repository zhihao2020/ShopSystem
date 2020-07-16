from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.add.addpeopleShoufaNum import Ui_Form
class addShouNum(QWidget,Ui_Form):
    Signal_FourParameter = pyqtSignal(list)
    def __init__(self,lis):
        super(addShouNum,self).__init__()
        self.setupUi(self)
        self.comboBox.addItems(lis)
        self.pushButton.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text().strip()
        phone = self.lineEdit.text().strip()
        shouName= self.comboBox.currentText()
        num = self.spinBox_2.value()
        lis =[name,phone,shouName,num]
        self.spinBox_2.setValue(0)
        self.Signal_FourParameter[list].emit(lis)

