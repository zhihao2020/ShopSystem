from UI.add.addpeopleMoney import Ui_Form
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.add.addpeopleMoney import Ui_Form

class addMoney(QWidget,Ui_Form):
    Signal_ThreeParameter = pyqtSignal(list)
    def __init__(self):
        super(addMoney,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        phone =self.lineEdit.text()
        money = self.doubleSpinBox.value()
        lis =[name,phone,money]
        self.doubleSpinBox.setValue(0)
        self.Signal_ThreeParameter[list].emit(lis)


