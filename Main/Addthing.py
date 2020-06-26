from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.AddThings import Ui_Form
class addThing(QWidget,Ui_Form):
    Signal_FivesParameter = pyqtSignal(list)
    def __init__(self):
        super(addThing,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        kind = self.comboBox.currentText()
        price = self.doubleSpinBox.value()
        num = self.spinBox.value()
        beizhu = self.lineEdit.text()
        lis =[name,kind,price,num,beizhu]
        self.Signal_FivesParameter[list].emit(lis)



