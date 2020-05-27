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
import pickle
import os

from Main.connectPrinter import Printmain

logging.basicConfig(filename='ProgramLog.log',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s:')

class reload_mainWin(QMainWindow,Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)
        self.ThingsList = []
        self.handList = []

        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName(r"..\data\all.db")

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)

        self.add_things.triggered.connect(self.addInformation)
        self.action_2.triggered.connect(self.addPeople_init)

        self.action.triggered.connect(self.about)
        self.look_Cust.triggered.connect(self.lookCust)

        # 按钮
        self.pushButton_2.clicked.connect(self.jiesuan)
        self.pushButton.clicked.connect(self.init_find)
        # 触发
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        self.cust_name.textChanged.connect(self.showThings2)
        self.cust_phone.textChanged.connect(self.showThings2)

        # 初始化
        self.showThings()
        self.index = 0
        # 窗口
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

    def get_Row(self):
        n = 0
        self.query.exec_("SELECT 名称 from things ")
        while(self.query.next()):
            n += 1
        print("数据库中有",n,"行")
        return n

    def showThings(self):
        #目标是商品的数据库
        self.openDB()
        self.showYaopin.setColumnCount(6)
        self.showYaopin.setRowCount(self.get_Row())
        self.showYaopin.setColumnWidth(0,50)
        self.showYaopin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showYaopin.setHorizontalHeaderLabels(["","名称","单价","备注","库存数量","数量"])
        self.showYaopin.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应

        self.query.exec_("SELECT 名称 from things ")
        i = 0
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

        r = open(r"F:\XUUse\data\shoufa.io","r")
        tempdata = open(r"..\data\custshoufa.ini","rb")
        d = pickle.load(tempdata)
        rs = r.read().split(',')
        print(rs)
        print("手法多少：",len(rs)-1)
        self.openDB()
        self.showShoufa.setColumnCount(6)
        self.showShoufa.setRowCount(len(rs)-1)
        self.showShoufa.setColumnWidth(0, 50)
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showShoufa.setHorizontalHeaderLabels(["","名称","价格","备注","剩余次数","使用次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应

        try:
            i = 0
            for n in r: #n 手法名称
                print("手法名称", n)
                self.query.exec_("SELECT 价格,备注 from 手法 where 名称='%s'" %n)
                while (self.query.next()):
                    ck = QCheckBox()
                    Qs = QSpinBox()
                    print("第"+str(i)+"行")
                    self.showShoufa.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i,1,QTableWidgetItem(n))
                    self.showShoufa.setItem(i,2,QTableWidgetItem(self.query.value(0)))
                    self.showShoufa.setItem(i,3,QTableWidgetItem(self.query.value(1)))
                    self.showShoufa.setItem(i,4, QTableWidgetItem(d[self.cust_name.text()][n]))  #这里填充剩余手法次数
                    print(d[self.cust_name.text()])
                    self.showShoufa.setCellWidget(i,5, Qs)
                i += 1
        except (IndexError,KeyError):
            pass
        r.close()
        self.showShoufa.show()
        tempdata.close()
        self.db.close()

    def addInformation(self):
        self.addThingForm.Signal_FivesParameter.connect(self.addThing)
        self.addThingForm.setWindowModality(Qt.ApplicationModal)
        self.addThingForm.show()

    def addThing(self,lis):
        self.openDB()
        if lis[0] in self.handList or lis[0] in self.ThingsList:
            QMessageBox.critical(self, '警告', '将对该商品修改', QMessageBox.Yes|QMessageBox.Yes)
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
        self.addPeopleForm.Signal_SevenParameter.connect(self.addPeople)
        self.addPeopleForm.setWindowModality(Qt.ApplicationModal)
        self.addPeopleForm.show()

    def addPeople(self,lis):
        #[name,year,dianhua,shangpin,shoufaName,shoufaNum,jifen]
        #待解决这里问题没有处理
        name = []
        phone = []
        tempdata = open(r"data\custshoufa.ini","rb")
        d = pickle.load(tempdata)
        tempdata.close()
        self.openDB()
        self.query.exec_("select 姓名,电话 from 顾客")
        while (self.query.next()):
            name.append(self.query.value(0))
            phone.append(self.query.value(1))
        if lis[0] in name:
            QMessageBox.information(self, '提示', '将对该用户%s进行充值'%lis[0], QMessageBox.Yes)
            self.query.exec_("SELECT 商品余额,积分 from 顾客 where 姓名 ='%s'" % lis[0])
            while(self.query.next()):
                shangpin = float(self.query.value(0)) + float(lis[3])
                jifen = float(self.query.value(1)) + float(lis[6])
                self.query.exec_("update 顾客 set 商品余额='%s',积分='%s'where 姓名='%s'" % (shangpin,jifen,lis[0]))
                text = "update 顾客 set 商品余额='%s',积分='%s' where 姓名='%s'" % (shangpin,jifen,lis[0])
                logging.info('用户修改---%s' %text)
            num = d[lis[0]][lis[4]]
            f = open(r"data\custshoufa.ini","w")
            d[lis[0]][lis[4]] = int(num) + int(lis[5])
            pickle.dump(d, f)
            f.close()
        elif lis[1] in phone:
            QMessageBox.information(self, '提示', '将对该用户%s进行充值'%lis[1], QMessageBox.Yes)
            self.query.exec_("SELECT 商品余额,积分 from 顾客 where 姓名 ='%s'" % lis[0])
            while (self.query.next()):
                shangpin = float(self.query.value(0)) + float(lis[3])
                jifen = float(self.query.value(1)) + float(lis[6])
                self.query.exec_("update 顾客 set 商品余额='%s',积分='%s'where 姓名='%s'" % (shangpin, jifen, lis[0]))
                text = "update 顾客 set 商品余额='%s',积分='%s' where 姓名='%s'" % (shangpin, jifen, lis[0])
                logging.info('用户修改---%s' % text)
            num = d[lis[0]][lis[4]]
            f = open(r"data\custshoufa.ini", "w")
            d[lis[0]][lis[4]] = int(num) + int(lis[5])
            pickle.dump(d, f)
            f.close()
        else:
            QMessageBox.information(self, '提示', '将添加新用户', QMessageBox.Yes|QMessageBox.Yes)
            self.query.exec_("insert into 顾客(姓名,年龄,电话,商品余额,积分) values('%s','%s','%s','%s','%s')" % (
            lis[0], lis[1], lis[2], lis[3],lis[6]))
            print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes| QMessageBox.Yes))
            text = "insert into 顾客(姓名,年龄,电话,商品余额,积分) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1], lis[2], lis[3],lis[6])
            logging.info('添加用户---%s' %text)
            data={}
            data[lis[4]] = lis[5]
            d[lis[0]] = data
            f = open(r"data\custshoufa.ini", "w")
            pickle.dump(d, f)
            f.close()
        self.db.close()
        tempdata.close()

    def lookCust(self):
        self.lookCust_Data.show()

    def connect_LCD(self):
        self.openDB()
        try:
            if self.cust_name.text():
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text())
            else :
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 电话=%s"%(self.cust_phone.text())
            self.query.exec_(MONERY)
            while(self.query.next()):
                self.money_vaild_2.display(self.query.value(0))
                self.jifen.display(self.query.value(1))
        except:
            pass
        self.db.close()

    def jiesuan(self, name):
        #手法结算待处理
        self.openDB()
        lines = []
        liness=[]
        flag =False
        flag2 = True
        di = {}
        diS={}
        sum = 0
        fin_Things = 0  # 最后应该缴纳的商品价钱
        log = []      # 购买记录
        logShoufa=[]
        i = 0
        tempdata = open(r"data\custshoufa.ini", "rb")
        d = pickle.load(tempdata)
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        if self.lineEdit_2.text() :
            while(i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append([self.showYaopin.cellWidget(i, 0), '商品',self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                              self.showYaopin.cellWidget(i, 5)])
                i += 1
            for line in lines:
                # 复选框、类别、名称、价格、数量
                if line[0].checkState() == Qt.Checked:
                    print(line[2].text())
                    fin_Things += float(line[3].text()) * float(line[4].value())
                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典
                    sum += float(line[3].text()) * float(line[4].value())
                    log.append([line[2].text(),line[3].text(),line[4].value()]) #购买记录[[a,b,a],[c,d,v]] 名称、价格、数量

            while (i < self.showShoufa.rowCount()):
                # 复选框、名称、价格、备注、剩余次数、使用次数
                liness.append(
                    [self.showShoufa.cellWidget(i, 0), '商品', self.showShoufa.item(i, 1), self.showShoufa.item(i, 4),
                     self.showShoufa.cellWidget(i, 5)])
                i += 1
            tempList=[]
            for line in liness:
                # 复选框、名称、剩余次数、使用次数
                if line[0].checkState() == Qt.Checked:
                    tempList.append(line[1].text()+":"+line[3].text())
                    diS[line[1].text()] = [int(line[2].value()),int(line[3].value())]  # 加入已选的名称和 剩余、使用 构成字典
                    logShoufa.append([line[1].text(), line[3].value()])  # 购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
            s = '\n'.join(tempList)
            fin = sum
            reply = QMessageBox.information(self, '提示', '消费金额%s\n,使用手法:%s' % (fin,s), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            tempdata.close()
            if reply == QMessageBox.Yes:
                for nameShoufa in diS.keys():
                    if diS[nameShoufa][0]- diS[nameShoufa][1] > 0:
                        shoufanum = diS[nameShoufa][0]- diS[nameShoufa][1]
                        d[self.cust_name][nameShoufa] = shoufanum
                        f = open(r"data\custshoufa.ini", "w")
                        pickle.dump(d,f)
                        f.close()
                    else:
                        print(QMessageBox.critical(self, '警告', '%s手法剩余次数不足\n现有库存%s' % (nameShoufa ,diS[nameShoufa][0])
                                                   ,QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes))
                        flag2 = False
                        break
                if flag2 == False:
                    for name in di.keys():
                        print(1)
                        self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                        while (self.query2.next()):
                            print(2)
                            if (float(self.query2.value(0)) - di[name] < 0):
                                print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                            else:
                                self.query.exec_("SELECT 积分,药品可用金额 from 顾客 where 姓名 = '%s'" % self.cust_name.text())
                                while (self.query.next()):

                                    if float(self.query.value(1)) - float(fin_Things)<0:
                                        print(QMessageBox.critical(self, '警告',
                                                                   '%商品余额不足\n购买商品余额%s' % (name, self.query2.value(1)),
                                                                   QMessageBox.Yes, QMessageBox.Yes))
                                    else:
                                        jifen = float(self.query.value(0)) + float(fin_Things)
                                        keyongThing = float(self.query.value(1)) - float(fin_Things)
                                        print("药品%s-%s=%s" % (float(self.query.value(1)), float(fin_Things),float(self.query.value(1)) - float(fin_Things)))
                                        kucunshuliang = self.query2.value(0)
                                        print(kucunshuliang)
                                        flag = True
                                        logging.info("%s消费 %s" % (self.cust_name.text(), fin))


                if flag:
                    self.query.exec_("update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'"
                                 % (jifen, keyongThing, self.cust_name.text()))
                    text = "update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'"% (jifen, keyongThing, self.cust_name.text())
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
                    self.db.close()
                    Printmain(log,logShoufa,fin,keyongThing)  # 打印小票信息

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