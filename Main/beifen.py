from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlTableModel,QSqlQueryModel,QSqlError,QSqlField
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import csv
from PyQt5 import QtCore
import sys
from UI.MainWindow import Ui_mainWindow

class reload_mainWin(QMainWindow,Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)

        #连接数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName('../data/all.db')
        self.db.open()

        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)
        self.print_things.triggered.connect(self.publish)
        self.add_things.triggered.connect(self.addThing)
        self.edit_things.triggered.connect(self.editThng)
        self.get_all_activities.triggered.connect(self.getAll)
        self.menu_4.triggered.connect(self.about)

        #按钮
        self.pushButton_2.clicked.connect(self.jiesuan)

        #触发查询
        self.thing_name.textChanged.connect(self.find_Thing)

        #触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)

        self.showThings()

    def about(self):
        pass

    def find_Thing(self):
        items = self.tableWidget.findItems(self.thing_name.text(), QtCore.Qt.MatchExactly)
        item = items[0]
        # 选中单元格
        item.setSelected( True)
        row = item.row()
        # 滚轮定位过去，快速定位到第17行
        self.tableWidget.verticalScrollBar().setSliderPosition(row)

        #刷新
    def reFreash(self):
        self.showThings()

    def get_Row(self):
        n = 0
        self.query.exec_("SELECT 名称 from 商品")
        while(self.query.next()):
            n += 1
        print("数据库中有",n,"行")
        return n

    def showThings(self):
        print("------进入tablewidget-------")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(self.get_Row())
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["","名称","单价","备注","数量"])
        self.tableWidget.
        i = 0
        self.query.exec_("SELECT 名称 from 商品")
        while(self.query.next()):

            print("商品名称",self.query.value(0))
            self.query2.exec_("SELECT 名称,单价,备注 from 商品 where 名称='%s'"%self.query.value(0))
            print("SELECT 名称,单价,备注 from 商品 where 名称='%s'"%self.query.value(0))
            while(self.query2.next()):
                for n in range(3):
                    print("第",i,"行，","第",n,"列")
                    ck = QCheckBox()
                    Qs= QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    print(self.query2.value(n))
                    self.tableWidget.setCellWidget(i,0,ck)
                    self.tableWidget.setItem(i,n+1,newItem)
                    self.tableWidget.setCellWidget(i,4,Qs)
            i+=1

        self.tableWidget.show()



    def publish(self):
        pass

    def addThing(self):
        pass

    def editThng(self):
        pass

    def importCsv(self):
        pass

    def jiesuan(self):
        pass

    def getAll(self):
        pass

    def connect_LCD(self):
        if self.cust_name.text():
            MONERY = "SELECT 可用金额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text())

        else :
            MONERY = "SELECT 可用金额,积分 from 顾客 where 电话='%s'"%(self.cust_phone.text())
        print(MONERY)
        self.query.exec_("连接LCD\n",MONERY)
        while(self.query.next()):
            self.money_vaild.display(self.query.value(0))
            self.jifen.display(self.query.value(1))
    #关闭数据库
    def closeEvent(self):
        self.db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWin = reload_mainWin()

    myWin.show()
    sys.exit(app.exec_())