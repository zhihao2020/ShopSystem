from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlTableModel,QSqlQueryModel,QSqlError,QSqlField
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import csv
from PyQt5 import QtCore
import sys
from UI.MainWindow import Ui_mainWindow
from Main.Addthing import addThing

class reload_mainWin(QMainWindow,Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)

        self.init()

    def init(self):
        # 连接数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName('../data/all.db')
        self.db.open()

        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)
        self.print_things.triggered.connect(self.publish)
        self.add_things.triggered.connect(self.add_Thing)
        self.edit_things.triggered.connect(self.edit_Thng)
        self.get_all_activities.triggered.connect(self.getAll)
        self.menu_4.triggered.connect(self.about)

        # 按钮
        self.pushButton_2.clicked.connect(self.jiesuan)

        # 触发查询
        self.thing_name.textChanged.connect(self.find_Thing)

        # 触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        #初始化
        self.showThings()
        self.index = 0
        self.tabWidget.currentChanged['int'].connect(self.changeItems)
        # 盛放 已选项目名称的list
        self.di = {}
        self.shoufa_list = []

    def changeItems(self,index):
        if self.index == 0:
            self.showThings()
        if self.index == 1:
            self.name_vaild.setText("次数")
            self.showThings2()
            self.connect_LCD()

    def about(self):
        pass

    def find_Thing(self):
        if self.index == 0:
            try:
                items = self.showYaopin.findItems(self.thing_name.text(), QtCore.Qt.MatchExactly)
                item = items[0]
                # 选中单元格
                item.setSelected(True)
                row = item.row()
                # 滚轮定位过去，快速定位到第17行
                self.showYaopin.verticalScrollBar().setSliderPosition(row)
            except:
                pass
        elif self.index == 1:
            try:
                items = self.showShoufa.findItems(self.thing_name.text(), QtCore.Qt.MatchExactly)
                item = items[0]
                # 选中单元格
                item.setSelected(True)
                row = item.row()
                # 滚轮定位过去，快速定位到第17行
                self.showShoufa.verticalScrollBar().setSliderPosition(row)
            except:
                pass

        #刷新TabWidget
    def reFreash(self):
        if self.index == 0:
            self.showThings()
        elif self.index == 1:
            self.showThings2()

    def get_Row(self):
        n = 0
        self.query.exec_("SELECT 名称 from 商品")
        while(self.query.next()):
            n += 1
        print("数据库中有",n,"行")

        return n

    def showThings(self):
        print("------进入tablewidget-------")
        self.showYaopin.setColumnCount(6)
        self.showYaopin.setRowCount(self.get_Row())
        self.showYaopin.setColumnWidth(0,50)
        self.showYaopin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showYaopin.setHorizontalHeaderLabels(["","名称","单价","备注",'库存数量',"数量"])
        self.showYaopin.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应
        i = 0
        self.query.exec_("SELECT 名称 from 商品")
        while(self.query.next()):

            print("商品名称",self.query.value(0))
            self.query2.exec_("SELECT 名称,单价,备注,数量 from 商品 where 名称='%s'"%self.query.value(0))
            print("SELECT 名称,单价,备注 from 商品 where 名称='%s'"%self.query.value(0))
            while(self.query2.next()):
                for n in range(4):
                    print("第",i,"行，","第",n,"列")
                    ck = QCheckBox()
                    Qs= QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    print(self.query2.value(n))
                    self.showYaopin.setCellWidget(i,0,ck)
                    self.showYaopin.setItem(i,n+1,newItem)
                    self.showYaopin.setCellWidget(i,5,Qs)
            i+=1
        self.showYaopin.show()

    def getRow(self):
        n = 0
        result = self.query.exec_("PRAGMA table_info([手法])")
        for column in result:
            self.shoufa_list.append(column['name'])
            n += 1
        return n-1

    def showThings2(self):
        print("-------手法————QTableWidget---------")
        self.showShoufa.setColumnCount(4)
        self.showShoufa.setColumnCount(6)
        self.showShoufa.setRowCount(self.getRow())
        self.showShoufa.setColumnWidth(0, 50)
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showShoufa.setHorizontalHeaderLabels(["","名称","所剩次数","使用次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应

        for i in self.shoufa_list:
            for j in range(4):
                print("第",i,"行，","第",j,"列")
                self.query2.exec_("SELECT '%s' from 手法 where 姓名='%s'"%(i,self.cust_name))
                while(self.query2.next()):
                    ck = QCheckBox()
                    Qs = QSpinBox()
                    newItem1 = QTableWidgetItem(str(i))
                    newItem2 = QTableWidgetItem(str(self.query2.value(0)))
                    self.showYaopin.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i,1,)
                    self.showYaopin.setItem(i,2, newItem2)
                    self.showYaopin.setCellWidget(i, 3, Qs)
        self.showShoufa.show()

    def publish(self):
        pass

    def add_Thing(self):
        pass

    def edit_Thng(self):
        pass

    def importCsv(self):
        pass

    def connect_LCD(self):
        if self.index == 0:
            try:
                if self.cust_name.text():
                    MONERY = "SELECT 可用金额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text())

                else :
                    MONERY = "SELECT 可用金额,积分 from 顾客 where 电话='%s'"%(self.cust_phone.text())
                print("连接LCD\n",MONERY)
                self.query.exec_(MONERY)
                while(self.query.next()):
                    self.money_vaild.display(self.query.value(0))
                    self.jifen.display(self.query.value(1))
            except:pass
        elif self.index == 1:
            pass

    def jiesuan(self, name):
        lines = []
        sum = 0
        i = 0
        if (i < self.name.rowCount()):
            lines.append([self.tableWidget.cellWidget(i, 0), self.tableWidget.item(i, 1), self.tableWidget.item(i, 2),
                          self.tableWidget.cellWidget(i, 5)])
            i += 1
        for line in lines:
            if line[0].isChecked():
                self.di[line[1].text()] = float(line[3].value)  # 加入已选的名称
                sum += float(line[2].text()) * float(line[3].value())

        print(sum)
        print("最后价格：", sum * float(self.lineEdit_4.text()))
        fin = sum * float(self.lineEdit_4.text())

        pan = 0

        if self.cust_name.text():
            pan = 1
        elif self.cust_phone.text():
            pan = 2
        else:
            pan = 3
            print(QMessageBox.information(self, '提示', '结算 进入 散客模式', QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No))
        reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:

            if pan == 1:
                self.query.exec_("SELECT 积分,可用金额,累计金额 from 商品 where 姓名 = '%s'" % self.cust_name.text())
                # 更改商品信息
                for name in self.Di.keys():
                    print("结算", name)
                    self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                    while (self.query2.next()):
                        if (float(self.query2.value(0)) - self.Di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                              % (float(self.query2.value(0)) - self.Di[name], name))
                # 更改用户信息
                while (self.query.next()):
                    jifen = self.query.value(0)
                    keyong = self.query.value(1)
                    leiji = self.query.value(2)

                self.query.exec_("update 顾客 set 积分 = '%s',可用金额='%s',累计金额='%s' where 姓名 ='%s'"
                                 % (jifen, keyong, leiji, self.cust_name.text()))

            elif pan == 2:
                self.query.exec_("SELECT 积分,可用金额,累计金额 from 商品 where 电话 = '%s'" % self.cust_phone.text())

                for name in self.Di.keys():
                    print("结算", name)
                    self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                    while (self.query2.next()):
                        if (float(self.query2.value(0)) - self.Di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                              % (float(self.query2.value(0)) - self.Di[name], name))

                while (self.query.next()):
                    jifen = self.query.value(0)
                    keyong = self.query.value(1)
                    leiji = self.query.value(2)

                self.query.exec_("update 顾客 set 积分 = '%s',可用金额='%s',累计金额='%s' where 电话 ='%s'" % (
                    jifen, keyong, leiji, self.cust_phone.text()))
                self.query.exec_()

            else:
                for name in self.Di.keys():
                    print("结算", name)
                    self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                    while (self.query2.next()):
                        if (float(self.query2.value(0)) - self.Di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                              % (float(self.query2.value(0)) - self.Di[name], name))

    #关闭数据库
    def closeEvent(self):
        self.db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWin = reload_mainWin()

    myWin.show()
    sys.exit(app.exec_())