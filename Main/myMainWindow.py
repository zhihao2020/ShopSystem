from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys
import webbrowser
from UI.MainWindow import Ui_mainWindow
from Main.Addpeople import addPeople
from Main.Addthing import addThing
from Main.customerData import lookCustData
import datetime
import logging
from Main.connectPrinter import Printmain

logging.basicConfig(filename='ProgramLog.log',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s:')

class reload_mainWin(QMainWindow,Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)
        self.ThingsList = []
        self.handList = []
        self.init()

    def init(self):
        # 连接数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName('../data/all.db')

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)

        self.add_things.triggered.connect(self.addInformation)
        self.action_2.triggered.connect(self.addPeople_init)
        self.edit_things.triggered.connect(self.editThing)
        self.action.triggered.connect(self.about)
        self.look_Cust.triggered.connect(self.lookCust)

        # 按钮
        self.pushButton_2.clicked.connect(self.jiesuan)
        self.pushButton.clicked.connect(self.init_find)
        # 触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        #初始化
        self.showThings()
        self.showThings2()
        self.tabWidget.currentChanged['int'].connect(self.currentTab)
        self.index = 0
        #窗口
        self.addThingForm = addThing()
        self.lookCust_Data = lookCustData()
        self.addPeopleForm = addPeople()

    def openDB(self):
        self.db.open()
        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
            logging.error("数据库连接失败，请查看数据库配置")
        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)

    def about(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def currentTab(self, index):
        if index == 0:
            self.index = 0
        elif index == 1:
            self.index = 1

    def init_find(self):
        self.find_Thing(self.thing_name.text())

    def find_Thing(self,name):
        #因为这是linetext changed触发的，所以此处加上异常处理
        if self.index == 0:
            try:
                items = self.showYaopin.findItems(name, QtCore.Qt.MatchExactly)
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
        #重新刷新
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
        self.openDB()
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
            self.ThingsList.append(self.query.value(0))
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
        self.db.close()

    def showThings2(self):
        #目标是手法的数据库
        self.openDB()
        self.showShoufa.setColumnCount(5)
        self.showShoufa.setRowCount(self.get_Row('手法'))
        self.showShoufa.setColumnWidth(0, 50)
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showShoufa.setHorizontalHeaderLabels(["","名称","价格","备注","次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应

        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='手法'")
        while (self.query.next()):
            print("手法名称", self.query.value(0))
            self.handList.append(self.query.value(0)) #保存手法的名录
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
        self.db.close()

    def addInformation(self):
        self.addThingForm.Signal_FivesParameter.connect(self.addThing)
        self.addThingForm.setWindowModality(Qt.ApplicationModal)
        self.addThingForm.show()

    def addThing(self,lis):
        self.openDB()
        print(self.ThingsList)
        if lis[0] in self.handList or lis[0] in self.ThingsList:
            QMessageBox.critical(self, '警告', '将对该商品修改', QMessageBox.Yes)
            self.query.exec_("select 库存数量 from things where 名称='%s'" % lis[0])
            while(self.query.next()):
                num = float(self.query.value(0)) + float(lis[3])
                if lis[2]:
                    self.query.exec_("update things set 价格='%s',库存数量='%s' where 名称='%s'" %(lis[2],num,lis[0]))
                    text = "update things set 价格='%s',库存数量='%s' where 名称='%s'" %(lis[2],num,lis[0])
                    logging.info('修改商品----%s' % text)
                else:
                    self.query.exec_("update things set 库存数量='%s' where 名称='%s'" % (num,lis[0]))
                    text = "update things set 库存数量='%s' where 名称='%s'" % (num,lis[0])
                    logging.info('修改商品----%s' % text)
        else:
            print(QMessageBox.information(self, "提示", '将要添加商品', QMessageBox.Yes))
            self.query.exec_("insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1],lis[2],lis[3],lis[4]))
            text = "insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1],lis[2],lis[3],lis[4])
            print(QMessageBox.information(self,"提示",'添加成功',QMessageBox.Yes))
            logging.info('修改商品----%s'%text)

        self.db.close()

    def addPeople_init(self):
        self.addPeopleForm.Signal_FivesParameter.connect(self.addPeople)
        self.addPeopleForm.setWindowModality(Qt.ApplicationModal)
        self.addPeopleForm.show()

    def addPeople(self,lis):
        name = []
        phone = []
        self.openDB()
        self.query.exec_("select 姓名,电话 from 顾客")
        while (self.query.next()):
            name.append(self.query.value(0))
            phone.append(self.query.value(1))
        if lis[0] in name:
            QMessageBox.information(self, '提示', '将对该用户%s进行充值'%lis[0], QMessageBox.Yes)
            self.query.exec_("SELECT 手法余额,商品余额 from 顾客 where 姓名 ='%s'" % lis[0])
            while(self.query.next()):
                shoufa = float(self.query.value(0)) + float(lis[2])
                shangpin = float(self.query.value(1)) + float(lis[3])
                self.query.exec_("update 顾客 set 手法余额='%s',商品余额='%s' where 姓名='%s'" % (shoufa, shangpin,lis[0]))
                text = "update 顾客 set 手法余额='%s',商品余额='%s' where 姓名='%s'" % (shoufa, shangpin,lis[0])
                logging.info('用户修改---%s' %text)

        elif lis[1] in phone:
            QMessageBox.information(self, '提示', '将对该用户%s进行充值'%lis[1], QMessageBox.Yes)
            self.query.exec_("SELECT 手法余额,商品余额 from 顾客 where 姓名 ='%s'"%lis[0])
            while(self.query.next()):
                shoufa = float(self.query.value(0)) +float(lis[2])
                shangpin = float(self.query.value(1)) +float(lis[3])
                self.query.exec_("update 顾客 set 手法余额='%s',商品余额='%s' where 姓名='%s'" % (
                    shoufa, shangpin,lis[0]))
                text = "update 顾客 set 手法余额='%s',商品余额='%s' where 姓名='%s'" % (shoufa, shangpin,lis[0])
                logging.info('用户修改---%s' %text)
        else:
            QMessageBox.information(self, '提示', '将添加新用户', QMessageBox.Yes|QMessageBox.Yes)
            self.query.exec_("insert into 顾客(姓名,年龄,电话,手法余额,商品余额) values('%s','%s','%s','%s','%s')" % (
            lis[0], lis[1], lis[2], lis[3],lis[4]))
            print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes| QMessageBox.Yes))
            text = "insert into 顾客(姓名,年龄,电话,手法余额,商品余额) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1], lis[2], lis[3],lis[4])
            logging.info('添加用户---%s' %text)
        self.db.close()

    def editThing(self):
        pass

    def lookCust(self):
        self.lookCust_Data.show()

    def connect_LCD(self):
        self.openDB()
        try:
            if self.cust_name.text():
                MONERY = "SELECT 药品可用金额,手法可用余额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text())

            else :
                MONERY = "SELECT 药品可用金额,手法可用余额,积分 from 顾客 where 电话=%s"%(self.cust_phone.text())
            self.query.exec_(MONERY)
            while(self.query.next()):
                self.money_vaild_2.display(self.query.value(0))
                self.money_vaild.display(self.query.value(1))
                self.jifen.display(self.query.value(2))
        except:
            pass
        self.db.close()

    def jiesuan(self, name):
        self.openDB()
        lines = []
        flag =False
        di = {}
        sum = 0
        sum_Hand = 0 #手法的总价
        sum_Things=0    #商品的总价
        fin_Hand = 0  # 最后应该缴纳的手法价钱
        fin_Things = 0  # 最后应该缴纳的商品价钱
        log = []      # 购买记录
        i = 0
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        if self.lineEdit_2.text() :
            while(i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append([self.showYaopin.cellWidget(i, 0), '商品',self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                              self.showYaopin.cellWidget(i, 5)])
                i += 1
            i=0
            while(i < self.showShoufa.rowCount()):
                lines.append([self.showShoufa.cellWidget(i, 0), '手法',self.showShoufa.item(i, 1), self.showShoufa.item(i, 2),
                              self.showYaopin.cellWidget(i, 5)])
                i+=1
            for line in lines:
                # 复选框、类别、名称、价格、数量
                if line[0].checkState() == Qt.Checked:
                    print(line[2].text())
                    if line[1] == '手法':
                        sum_Hand += float(line[3].text()) * float(line[4].value())
                        fin_Hand = sum_Hand * float(self.lineEdit.text())
                    if line[1] == '商品':
                        sum_Things += float(line[3].text()) * float(line[4].value())
                        fin_Things = sum_Things * float(self.lineEdit.text())
                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典
                    sum += float(line[3].text()) * float(line[4].value())
                    log.append([line[2].text(),line[3].text(),line[4].value()]) #购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
            fin = sum * float(self.lineEdit.text())
            reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                for name in di.keys():
                    print(1)
                    self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                    while (self.query2.next()):
                        print(2)
                        if (float(self.query2.value(0)) - di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            self.query.exec_("SELECT 积分,药品可用金额,手法可用余额 from 顾客 where 姓名 = '%s'" % self.cust_name.text())
                            while (self.query.next()):
                                if float(self.query.value(2)) - float(fin_Hand) < 0:
                                    print(QMessageBox.critical(self, '警告',
                                                               '%手法余额不足\n现有手法余额%s' % (name, self.query2.value(2)),
                                                               QMessageBox.Yes, QMessageBox.Yes))

                                elif float(self.query.value(1)) - float(fin_Things)<0:
                                    print(QMessageBox.critical(self, '警告',
                                                               '%商品余额不足\n购买商品余额%s' % (name, self.query2.value(1)),
                                                               QMessageBox.Yes, QMessageBox.Yes))

                                else:
                                    keyongHand = float(self.query.value(2)) - float(fin_Hand)
                                    print("手法%s-%s=%s"%(float(self.query.value(2)),float(fin_Hand),float(self.query.value(2)) - float(fin_Hand)))
                                    jifen = float(self.query.value(0)) + float(fin_Things)
                                    keyongThing = float(self.query.value(1)) - float(fin_Things)
                                    print("药品%s-%s=%s" % (float(self.query.value(1)), float(fin_Things),float(self.query.value(1)) - float(fin_Things)))
                                    kucunshuliang = self.query2.value(0)
                                    print(kucunshuliang)
                                    flag = True
                                    logging.info("%s消费 %s" % (self.cust_name.text(), fin))
                if flag:
                    self.query.exec_("update 顾客 set 积分 = '%s',药品可用金额='%s',手法可用余额='%s' where 姓名 ='%s'"
                                 % (jifen, keyongThing, keyongHand, self.cust_name.text()))
                    text = "update 顾客 set 积分 = '%s',药品可用金额='%s',手法可用余额='%s' where 姓名 ='%s'"% (jifen, keyongThing, keyongHand, self.cust_name.text())
                    logging.info(text)
                    #self.query.exec_("update 员工 set 时间 = '%s',记录='%s',金额='%s' where 工号 ='%s'"% (now, log, fin,self.))

                    #更改商品信息
                    self.query2.exec_("update things set 库存数量 = '%s' where 名称 ='%s'"
                                      % (float(kucunshuliang) - di[name], name))
                    text = "update things set 库存数量 = '%s' where 名称 ='%s'"% (float(kucunshuliang) - di[name], name)
                    logging.info(text)
                    # 提交到log数据表
                    if self.cust_name.text():
                        self.query.exec_(
                            'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")'
                            % (self.cust_name.text(), log, now, self.lineEdit_2.text(), fin))
                        text ='insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")'% (self.cust_name.text(), log, now, self.lineEdit_2.text(), fin)
                        logging.info(text)
                    elif self.cust_phone.text():
                        self.query.exec_('insert into log(电话,购买记录,购买时间,工号,金额)values("%s","%s","%s","%s","%s")'
                                         % (self.cust_phone.text(), log, now, self.lineEdit_2.text(),fin))
                        text = "insert into log(电话,购买记录,购买时间,工号,金额) values('%s','%s','%s','%s','%s')"% (self.cust_phone.text(), log, now, self.lineEdit_2.text(),fin)
                        logging.info(text)
                    Printmain(log, fin,keyongThing,keyongHand)  # 打印小票信息

        else:
            print(QMessageBox.information(self, '提示', '请输入员工工号', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes))
        self.db.close()

    #关闭数据库
    def closeEvent(self,event):
        self.db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())