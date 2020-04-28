from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from UI.AddThings import Ui_Form

class addThing(QWidget,Ui_Form):
    Signal_ThreeParameter = pyqtSignal(list)
    def __init__(self):
        super(addThing,self).__init__()
        self.setupUi(self)
        self.add_thing.clicked.connect(self.emitSingal)

    def emitSingal(self):
        name = self.add_thing_name.text()
        price = self.add_thing_price.text()
        beizhu = self.beizhu.text()
        lis =[name,price,beizhu]
        self.Signal_ThreeParameter[list].emit(lis)


