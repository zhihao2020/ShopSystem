from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.Addpeople import Ui_Form
class addPeople(QWidget,Ui_Form):
    Signal_SevenParameter = pyqtSignal(list)
    def __init__(self):
        super(addPeople,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        year = self.spinBox.value()
        dianhua = self.lineEdit.text()
        shangpin = self.doubleSpinBox_2.value()
        shoufaName = self.comboBox.currentText()
        shoufaNum = self.spinBox_2.value()
        jifen =self.lineEdit_2.text()

        if jifen == "":
            jifen = 0
        else:jifen = jifen

        lis =[name,year,dianhua,shangpin,shoufaName,shoufaNum,jifen]
        self.Signal_SevenParameter[list].emit(lis)


