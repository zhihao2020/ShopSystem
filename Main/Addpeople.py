from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.add.addPeople import  Ui_Form
class addPeople(QWidget,Ui_Form):
    Signal_FourParameter = pyqtSignal(list)
    def __init__(self):
        super(addPeople,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        year = self.spinBox.value()
        dianhua = self.lineEdit.text()
        birthDay = self.dateEdit.text()
        print(birthDay)
        lis =[name,year,dianhua,birthDay]
        self.Signal_FourParameter[list].emit(lis)


