from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.Addpeople import Ui_Form
class addPeople(QWidget,Ui_Form):
    Signal_FivesParameter = pyqtSignal(list)
    def __init__(self):
        super(addPeople,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        year = self.spinBox.value()
        dianhua = self.lineEdit.text()
        shoufa = self.doubleSpinBox.value()
        shangpin = self.doubleSpinBox_2.value()
        lis =[name,year,dianhua,shoufa,shangpin]
        self.Signal_FivesParameter[list].emit(lis)


