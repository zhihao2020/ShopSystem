from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlTableModel,QSqlQueryModel,QSqlError,QSqlField
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys
import webbrowser
from UI.MainWindow import Ui_mainWindow
from Main.Addthing import addThing
from Main.customerData import lookCustData
import datetime
import logging

logging.basicConfig(filename='ProgramLog.txt',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
            logging.error("数据库连接失败，请查看数据库配置")
        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)
        self.print_things.triggered.connect(self.printXiaopiao)
        self.add_things.triggered.connect(self.addInformation)
        self.action_2.triggered.connect(self.addPeople)
        self.edit_things.triggered.connect(self.editThing)
        self.action.triggered.connect(self.about)
        self.look_Cust.triggered.connect(self.lookCust)

        # 按钮
        self.pushButton_2.clicked.connect(self.jiesuan)

        # 触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        #初始化
        self.showThings()
        self.showThings2()
        self.tabWidget.currentChanged['int'].connect(self.currentTab)

        # 触发查询
        self.thing_name.textChanged.connect(self.find_Thing)
        self.index = 0

        #窗口
        self.addThingForm = addThing()
        self.lookCust_Data = lookCustData()

    def about(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def currentTab(self, index):
        if index == 0:
            self.index = 0
        elif index == 1:
            self.index = 1

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
        self.showThings()
        self.showThings2()

    def get_Row(self,kind):
        n = 0
        self.query.exec_("SELECT 名称 from things where 类别='{}'".format(kind))
        while(self.query.next()):
            n += 1
        print("数据库中有",n,"行")
        return n

    def showThings(self):
        #目标是商品的数据库
        self.showYaopin.setColumnCount(6)
        self.showYaopin.setRowCount(self.get_Row('商品'))
        self.showYaopin.setColumnWidth(0,50)
        self.showYaopin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showYaopin.setHorizontalHeaderLabels(["","名称","单价","备注","库存数量","数量"])
        self.showYaopin.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='商品'")
        while(self.query.next()):
            print("商品名称",self.query.value(0))
            self.query2.exec_("SELECT 名称,价格,备注,库存数量 from things where 名称='%s'"%self.query.value(0))
            print("SELECT 名称,价格,备注 from things where 名称='%s'"%self.query.value(0))
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

    def showThings2(self):
        #目标是手法的数据库
        self.showShoufa.setColumnCount(5)
        self.showShoufa.setRowCount(self.get_Row('手法'))
        self.showShoufa.setColumnWidth(0, 50)
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showShoufa.setHorizontalHeaderLabels(["","名称","价格","备注","次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应

        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='手法'")
        while (self.query.next()):
            print("商品名称", self.query.value(0))
            self.query2.exec_("SELECT 名称,价格,备注 from things where 名称='%s'" % self.query.value(0))
            while (self.query2.next()):
                for n in range(3):
                    print("第", i, "行，", "第", n, "列")
                    ck = QCheckBox()
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    print(self.query2.value(n))
                    self.showShoufa.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i, n + 1, newItem)
                    self.showShoufa.setCellWidget(i,4, Qs)
            i += 1
        self.showShoufa.show()

    def printXiaopiao(self):
        pass

    def addInformation(self):
        self.addThingForm.Signal_FivesParameter.connect(self.addThing)
        self.addThingForm.setWindowModality(Qt.ApplicationModal)
        self.addThingForm.show()

    def addThing(self,lis):
        reply = QMessageBox.information(self, '提示', '数据将会被添加', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            #加入验证 避免反复添加
            if self.query.exec_("select 名称 from things where 名称='%s'"%lis[0]):
                QMessageBox.critical(self, '警告', '请勿重复添加', QMessageBox.Yes)
            else:
                self.query.exec_("insert into things(名称,类别,价格,库存,备注) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1],lis[2],lis[3],lis[4]))
                print(QMessageBox.information(self,"提示",'添加成功',QMessageBox.Yes))
                logging.info('添加商品%s'%lis[0])

    def editThing(self):
        pass

    def lookCust(self):
        self.lookCust_Data.show()

    def addPeople(self):
        pass

    def connect_LCD(self):
        try:
            if self.cust_name.text():
                MONERY = "SELECT (药品)可用金额,(手法)可用金额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text())

            else :
                MONERY = "SELECT (药品)可用金额,(手法)可用金额,积分 from 顾客 where 电话='%s'"%(self.cust_phone.text())
            print("连接LCD\n",MONERY)
            self.query.exec_(MONERY)
            while(self.query.next()):
                self.money_vaild_2.display(self.query.value(0))
                self.money_vaild.display(self.query.value(1))
                self.jifen.display(self.query.value(2))
        except:
            pass

    def jiesuan(self, name):
        lines = []
        di = {}
        sum = 0
        sum_Hand = 0 #手法的总价
        sum_Things=0    #商品的总价
        log = []      # 购买记录
        i = 0
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        if self.lineEdit_2.text() :
            while(i < self.showYaopin.rowCount()):
                # 复选框、名称、价格、数量
                lines.append([self.showYaopin.cellWidget(i, 0), '商品',self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                              self.showYaopin.cellWidget(i, 5)])
                i += 1
            while(i < self.showShoufa.rowCount()):
                lines.append([self.showShoufa.cellWidget(i, 0), '手法',self.showShoufa.item(i, 1), self.showShoufa.item(i, 2),
                              self.showYaopin.cellWidget(i, 4)])
                i+=1
            for line in lines:
                if line[0].checkState() == Qt.Checked:
                    if line[1].text() == '手法':
                        sum_Things += float(line[3].text()) * float(line[4].Value())
                        fin_Things = sum_Things * float(self.lineEdit.text())
                    if line[1].text() == '商品':
                        sum_Hand += float(line[3].text()) * float(line[4].Value())
                        fin_Hand = sum_Hand * float(self.lineEdit.text())
                    di[line[1].text()] = float(line[3].Value())  # 加入已选的名称
                    sum += float(line[2].text()) * float(line[3].Value())
                    log += [line[1].text(),line[2].text(),line[3].text()] #购买记录[[a,b,a],[c,d,v]]
            fin = sum * float(self.lineEdit.text())
            reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                logging.info('产生消费记录')
                #提交到log数据表
                if self.cust_name.text():
                    self.query.exec_("insert into log(顾客姓名,购买记录,购买时间,工号,金额) values('%s','%s','%s','%s')"
                                     % (self.cust_name.text(),log,now,self.lineEdit_2.text(),fin))
                elif self.cust_phone.text():
                    self.query.exec_("insert into log(电话,购买记录,购买时间,工号) values('%s','%s','%s','%s')"
                                     % (self.cust_phone.text(), log, now, self.lineEdit_2.text()))
                for name in di.keys():
                    print("结算", name)
                    self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                    if (float(self.query2.value(0)) - di[name] < 0):
                        print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                    else:
                        #更改商品信息
                        self.query2.exec_("update things set 库存数量 = '%s' where 名称 ='%s'"
                                          % (float(self.query2.value(0)) - di[name], name))
                # 更改用户信息
                self.query.exec_("SELECT 积分,(药品)可用金额,(手法)可用金额 from 顾客 where 姓名 = '%s'" % self.cust_name.text())

                try:
                    jifen = float(self.query.value(0)) + float(fin_Things)
                    keyongHand = float(self.query.value(2)) - float(fin_Hand)
                except:
                    logging.info('这次消费没有手法')
                    pass
                keyongThing = float(self.query.value(1)) - float(fin_Things)
                #更改顾客信息（顾客数据表）
                self.query.exec_("update 顾客 set 积分 = '%s',(药品)可用金额='%s',(手法)可用金额='%s' where 姓名 ='%s'"
                                 % (jifen, keyongThing,keyongHand ,self.cust_name.text()))
                self.query.exec_("update 员工 set 时间 = '%s',记录='%s',金额='%s' where 工号 ='%s'"
                                 % (now, log,fin,))
        else:print(QMessageBox.information(self, '提示', '请输入员工工号' , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes))

    #关闭数据库
    def closeEvent(self,event):
        self.db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())