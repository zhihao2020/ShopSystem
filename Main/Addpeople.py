from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.addPeople import  Ui_Form
class addPeople(QWidget,Ui_Form):
    Signal_SixParameter = pyqtSignal(list)
    def __init__(self,shoufa_list=None):
        super(addPeople,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)
        self.comboBox.addItems(shoufa_list)
    def emitSingal(self):
        name = self.add_thing_name.text()
        year = self.spinBox.value()
        dianhua = self.lineEdit.text()
        shoufa = self.comboBox.currentText()
        shoufa_cishu = self.spinBox_2.value()
        shangpin = self.doubleSpinBox_2.value()
        lis =[name,year,dianhua,shoufa,shoufa_cishu,shangpin]
        self.Signal_SixParameter[list].emit(lis)


