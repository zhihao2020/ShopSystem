from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import sys
import webbrowser
from pygame import mixer
from UI.MainWindow import Ui_mainWindow
from Addpeople import addPeople
from Addthing import addThing
from AddpeopleMoney import addMoney
from ChangeZhekou import ChangePrice
from customerData import lookCustData
from addpeopleNum import addShouNum
import datetime
import logging
from  connectPrinter import Printmain

logging.basicConfig(filename='ProgramLog.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s:')

class reload_mainWin(QMainWindow,Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin,self).__init__()
        self.setupUi(self)
        self.ThingsList = []
        self.handList = []
        self.init()
        self.birthDayMusic()

    def init(self):
        # 连接数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE', "db2")
        self.db.setDatabaseName('data/all.db')

        # this is QAction
        self.refreash.triggered.connect(self.reFreash)
        self.add_things.triggered.connect(self.addInformation)
        self.look_Cust.triggered.connect(self.lookCust)
        self.action_5.triggered.connect(self.birthDayMusic)
        self.action_4.triggered.connect(self.init_addUserMoney)
        self.action_3.triggered.connect(self.init_addUserShouNum)
        self.action_2.triggered.connect(self.addPeople_init)
        self.action.triggered.connect(self.about)
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

    def openDB(self):
        self.db.open()
        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
            logging.error("数据库连接失败，请查看数据库配置")
        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)
        self.query3 = QSqlQuery(self.db)
    
    def about(self):
        webbrowser.open_new_tab('https://zhihao2020.github.io/about/')

    def birthDayMusic(self):
        self.openDB()
        tempText = ""
        self.query.exec_("SELECT 姓名,电话,生日 from 顾客 ")
        while (self.query.next()):
            if datetime.datetime.today().strftime('%m/%d') in self.query.value(2):
                tempText += "姓名:%s ,电话:%s ,生日:%s\n"%(self.query.value(0),self.query.value(1),self.query.value(2))
        if tempText != "":
            mixer.init()
            mixer.music.load(r"images\生日歌.mp3")
            mixer.music.play(loops=1, start=0.0)
            mixer.music.set_volume(1)
            QMessageBox.information(self,"提示",tempText,QMessageBox.Yes)

        self.db.close()

    def currentTab(self, index):
        if index == 0:
            self.index = 0
        elif index == 1:
            self.index = 1

    def init_find(self):
        self.find_Thing(self.thing_name.text().strip())

    def find_Thing(self,name):
        #因为这是linetext changed触发的，所以此处加上异常处理
        if self.index == 0:
            try:
                items = self.showYaopin.findItems(name, QtCore.Qt.MatchContains)
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
                items = self.showShoufa.findItems(self.thing_name.text().strip(), QtCore.Qt.MatchExactly)
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
        self.ThingsList = []
        self.handList = []
        self.showThings()
        self.showThings2()
        self.connect_LCD()

    def get_Row(self,kind):
        n = 0
        self.query.exec_("SELECT 名称 from things where 类别='{}'".format(kind))
        while(self.query.next()):
            n += 1
        #print("数据库中有",n,"行")
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
        self.showYaopin.itemDoubleClicked.connect(self.changPrize)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='商品'")
        while(self.query.next()):
            #print("商品名称",self.query.value(0))
            self.ThingsList.append(self.query.value(0))
            self.query2.exec_("SELECT 名称,价格,备注,库存数量 from things where 名称='%s'"%self.query.value(0))
            #print("SELECT 名称,价格,备注 from things where 名称='%s'"%self.query.value(0))
            while(self.query2.next()):
                for n in range(4):
                    #print("第",i,"行，","第",n,"列")
                    ck = QCheckBox()
                    Qs= QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    #print(self.query2.value(n))
                    self.showYaopin.setCellWidget(i,0,ck)
                    self.showYaopin.setItem(i,n+1,newItem)
                    self.showYaopin.setCellWidget(i,5,Qs)
            i+=1
        self.showYaopin.show()
        self.db.close()

    def showThings2(self):
        #目标是手法的数据库
        self.openDB()
        self.showShoufa.setColumnCount(6)
        self.showShoufa.setRowCount(self.get_Row('手法'))
        self.showShoufa.setColumnWidth(0, 50)
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showShoufa.setHorizontalHeaderLabels(["","名称","非会员价格","备注","剩余次数","次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格自适应
        #self.showShoufa.itemDoubleClicked.connect(self.changPrize)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='手法'")
        while (self.query.next()):
            print("手法名称", self.query.value(0))
            self.handList.append(self.query.value(0)) #保存手法的名录
            self.query2.exec_("SELECT 名称,价格,备注 from things where 名称='%s'" % self.query.value(0))
            while (self.query2.next()):
                for n in range(3):
                    #print("第", i, "行，", "第", n, "列")
                    ck = QCheckBox()
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    print(self.query2.value(n))
                    self.showShoufa.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i, n + 1, newItem)
                    self.query3.exec_("SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text().strip()))
                   # print("SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text()))
                    while (self.query3.next()):
                        self.showShoufa.setItem(i, 4, QTableWidgetItem(str(self.query3.value(0))))
                    self.showShoufa.setCellWidget(i, 5, Qs)
            i += 1
        self.showShoufa.show()
        self.db.close()

    def changPrize(self,item):
        #print(222)
        if self.index == 0:
            #print(12,self.showYaopin.item(item.row(),1).text())
            self.change_Pice = ChangePrice(self.showYaopin.item(item.row(),1).text(),self.showYaopin.item(item.row(),2).text(),item.row())
            self.change_Pice.Signal_TwoParameter.connect(self.changePrize2)
            self.change_Pice.setWindowModality(Qt.ApplicationModal)
            self.change_Pice.show()
        else :
            self.change_Pice = ChangePrice(self.showShoufa.item(item.row(),1).text(),self.showShoufa.item(item.row(),2).text(),item.row())
            self.change_Pice.Signal_TwoParameter.connect(self.changePrize2)
            self.change_Pice.setWindowModality(Qt.ApplicationModal)
            self.change_Pice.show()

    def changePrize2(self,li):
        if self.index == 0:
            self.showYaopin.setItem(li[1],2,QTableWidgetItem(li[0]))
        elif self.index == 1:
            self.showShoufa.setItem(li[1],2,QTableWidgetItem(li[0]))

    def addInformation(self):
        self.addThingForm = addThing()
        self.addThingForm.Signal_FivesParameter.connect(self.addThing)
        self.addThingForm.setWindowModality(Qt.ApplicationModal)
        self.addThingForm.show()

    def addThing(self,lis):
        #[name,kind,price,num,beizhu]
        self.openDB()
        print(self.ThingsList)
        if lis[0] in self.handList or lis[0] in self.ThingsList:
            reply = QMessageBox.critical(self, '警告', '将对该商品修改', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
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
            if lis[1] == "手法":
                reply = QMessageBox.information(self, "提示", '将要添加手法', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.query.exec_("insert into things(名称,类别,价格,备注) values('%s','%s','%s','%s')" % (
                    lis[0], lis[1], lis[2],  lis[4]))
                    self.query.exec_("alter table 顾客 add %s int;"%(lis[0]))
                    text = "alter table 顾客 add %s int;"%(lis[0])
                    print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes))
                    logging.info('添加商品----%s' % text)
            else:
                reply = QMessageBox.information(self, "提示", '将要添加商品', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.query.exec_("insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1],lis[2],lis[3],lis[4]))
                    text = "insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (lis[0], lis[1],lis[2],lis[3],lis[4])
                    print(QMessageBox.information(self,"提示",'添加成功',QMessageBox.Yes))
                    logging.info('添加商品----%s'%text)

        self.db.close()

    def addPeople_init(self):
        self.addPeopleForm = addPeople()
        self.addPeopleForm.Signal_FourParameter.connect(self.addPeople)
        self.addPeopleForm.setWindowModality(Qt.ApplicationModal)
        self.addPeopleForm.show()

    def addPeople(self,lis):
        #[name,year,dianhua]
        name = []
        phone = []
        self.openDB()
        self.query.exec_("select 姓名,电话 from 顾客")
        tempnum =0
        while (self.query.next()):
            name.append(self.query.value(0))
            phone.append(self.query.value(1))
            tempnum +=1
        if lis[0] in name or lis[1] in phone:
            QMessageBox.information(self, '提示', '该用户已经存在', QMessageBox.Yes)
        
        else:
            reply = QMessageBox.information(self, '提示', '将添加新用户\n 仅仅添加姓名:%s、年龄:%s、电话信息:%s'% (lis[0], lis[1], lis[2]), QMessageBox.Yes|QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.query.exec_("insert into 顾客(uid,姓名,年龄,电话,生日) values('%d','%s','%s','%s','%s')" % (tempnum,lis[0], lis[1], lis[2],lis[3]))
                print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes| QMessageBox.Yes))
                text = "insert into 顾客(uid,姓名,年龄,电话,生日) values('%d','%s','%s','%s','%s')" % (tempnum,lis[0], lis[1], lis[2],lis[3])
                logging.info('添加用户---%s' %text)
        self.db.close()

    def init_addUserMoney(self):
        self.addPeopleMoney = addMoney()
        self.addPeopleMoney.Signal_ThreeParameter.connect(self.addUserMoney)
        self.addPeopleMoney.setWindowModality(Qt.ApplicationModal)
        self.addPeopleMoney.show()

    def addUserMoney(self,lis):
        self.addPeopleMoney.setWindowModality(Qt.ApplicationModal)
        self.addPeopleMoney.show()
        self.openDB() #打开数据库连接
        self.query.exec_("select 姓名,电话 from 顾客")
        name = []
        phone = []
        while (self.query.next()):
            name.append(self.query.value(0))
            phone.append(self.query.value(1))
        if lis[0] in name:
            reply = QMessageBox.information(self, '提示', '将对该用户%s进行充值'%lis[0], QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.query.exec_("SELECT 药品可用金额 from 顾客 where 姓名 ='%s'" % lis[0])
                print("SELECT 药品可用金额 from 顾客 where 姓名 ='%s'" % lis[0])
                while(self.query.next()):
                    print(8688439)
                    shangpin = float(self.query.value(0)) + float(lis[2])
                    self.query.exec_("update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin,lis[0]))
                    text = "update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin,lis[0])
                    logging.info('用户修改---%s' %text)

        elif lis[1] in phone:
            reply = QMessageBox.information(self, '提示', '将对该用户%s 进行充值'%lis[1], QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.query.exec_("SELECT 药品可用金额 from 顾客 where 电话 ='%s'"%lis[1])
                while(self.query.next()):
                    shangpin = float(self.query.value(0)) +float(lis[2])
                    self.query.exec_("update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin,lis[1]))
                    text = "update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin,lis[1])
                    logging.info('用户修改---%s' %text)
        else:
            QMessageBox.information(self, '提示', '不存在该用户', QMessageBox.Yes|QMessageBox.Yes)
        self.db.close()

    def init_addUserShouNum(self):
        print("手法目录：",self.handList)
        self.addPeopleShouNum = addShouNum(self.handList)
        self.addPeopleShouNum.Signal_FourParameter.connect(self.addUserShouNum)
        self.addPeopleShouNum.setWindowModality(Qt.ApplicationModal)
        self.addPeopleShouNum.show()

    def addUserShouNum(self,lis):
        name = []
        phone = []
        self.openDB()
        self.query.exec_("select 姓名,电话 from 顾客")
        while (self.query.next()):
            name.append(self.query.value(0))
            phone.append(self.query.value(1))
        if lis[0] in name :#or lis[1] in phone:
            reply = QMessageBox.information(self, '提示', '对用户充值手法次数', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.query.exec_("select %s from 顾客 where 姓名='%s' or 电话='%s'"%(lis[2],lis[0],lis[1]))
                #print("select %s from 顾客 where 姓名='%s' or 电话='%s'"%(lis[2],lis[0],lis[1]))
                initNum =0
                while (self.query.next()):
                    initNum = self.query.value(0)
                    print(initNum)
                if not initNum:
                    initNum =0
                    #print(type(initNum))
                print(lis[3])
                Num = initNum + int(lis[3])
                print("Num ",Num)
                self.query.exec_("update 顾客 set %s='%s' where 姓名='%s'" % (lis[2], Num, lis[0]))
                text = "update 顾客 set %s='%s' where 姓名='%s'" % (lis[2], Num, lis[0])
                #print(text)
                logging.info('用户修改---%s' % text)
            else:pass
        else:
            QMessageBox.information(self, '提示', '该用户不存在', QMessageBox.Yes)
            
        self.db.close()
   
    def lookCust(self):
        self.lookCust_Data = lookCustData()
        self.lookCust_Data.show()

    def connect_LCD(self):
        self.openDB()
        try:
            if self.cust_name.text().strip():
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 姓名 = '%s'"%(self.cust_name.text().strip())
            else :
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 电话=%s"%(self.cust_phone.text().strip())
            self.query.exec_(MONERY)
            while(self.query.next()):
                self.money_vaild_2.display(self.query.value(0))
                self.jifen.display(self.query.value(1))
        except:
            pass
        self.db.close()

    def jiesuan(self, name):
        self.openDB()
        lines = []
        flag = False
        flag2 = False
        di = {}
        sum = 0
        sum_Things = 0  # 商品的总价
        HandList = []
        log = []      # 购买记录
        logtemp =[]
        Hand_FinList = []
        keyongThing=None
        jifen=0

        i = 0
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        if not self.cust_name.text().strip() and not self.cust_phone.text().strip():
            print(QMessageBox.information(self, '提示','进入非会员模式',QMessageBox.Yes, QMessageBox.Yes))
            while (i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append(
                    [self.showYaopin.cellWidget(i, 0), '商品', self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                     self.showYaopin.cellWidget(i, 5)])
                i+=1
            for line in lines:
                # 复选框、类别、名称、价格、数量
                if line[0].checkState() == Qt.Checked:
                    if line[1] == '商品':
                        sum_Things += float(line[3].text()) * float(line[4].value())

                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典
                    logtemp.append([line[2].text(),line[3].text(),line[4].value()])
                    log.append([line[2].text(),line[3].text(),line[4].value()]) #购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
            fin = sum_Things
            reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                for name in di.keys():
                    self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                    while (self.query2.next()):
                        if (float(self.query2.value(0)) - di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            kucunshuliang = self.query2.value(0)
                            #print(kucunshuliang)
                            flag = True
                            logging.info("%s消费 %s" % (self.cust_name.text().strip, fin))
                if flag:
                    #self.query.exec_("update 员工 set 时间 = '%s',记录='%s',金额='%s' where 工号 ='%s'"% (now, log, fin,self.))
                    #更改商品信息
                    self.query2.exec_("update things set 库存数量 = '%s' where 名称 ='%s'"% (float(kucunshuliang) - di[name], name))
                    text = "update things set 库存数量 = '%s' where 名称 ='%s'"% (float(kucunshuliang) - di[name], name)
                    logging.info(text)
                    # 提交到log数据表
                    Printmain(log, fin)  # 打印小票信息

        elif self.lineEdit_2.text() :
            i=0
            while(i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append([self.showYaopin.cellWidget(i, 0), '商品',self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                              self.showYaopin.cellWidget(i, 5)])
                i += 1
            i=0
            while(i < self.showShoufa.rowCount()):
                lines.append([self.showShoufa.cellWidget(i, 0), '手法', self.showShoufa.item(i, 1),
                              self.showShoufa.item(i, 4),self.showShoufa.cellWidget(i, 5)])
               #print(self.showShoufa.item(i, 4).text())
                i+=1
            for line in lines:
                # 复选框、类别、名称、使用次数、剩余数量
                if line[0].checkState() == Qt.Checked:
                    if line[1] == '手法':
                        # 复选框、类别、名称、次数、剩余次数
                        HandList.append(line)

                    if line[1] == '商品':
                        sum_Things += float(line[3].text()) * float(line[4].value())
                        log.append([line[2].text(),line[3].text(),line[4].value()]) #购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
                    logtemp.append([line[2].text(), line[3].text(), line[4].value()])
                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典

                    sum = sum_Things

            reply = QMessageBox.information(self, '提示', '消费金额%s' %sum, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                for Hand_num in HandList:
                    # 复选框、类别、名称、次数、剩余次数

                    if int(Hand_num[3].text()) - int(Hand_num[4].value()) < 0:
                        print(QMessageBox.information(self, '提示', '%s剩余次数不足' %Hand_num[2].text(), QMessageBox.Yes, QMessageBox.Yes))
                    else:
                        Rest_num = int(Hand_num[3].text()) - int(Hand_num[4].value())
                        Hand_FinList.append([Hand_num[2].text(),Rest_num,int(Hand_num[4].value())]) #名称、数量

                        flag2 = True

                for name in di.keys():
                    flag = False
                    self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                    while (self.query2.next()):
                        if not self.query2.value(0):
                            print("没有数量")
                            break
                        elif float(self.query2.value(0)) - di[name] < 0:
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                            break
                        else:
                            self.query.exec_("SELECT 积分,药品可用金额 from 顾客 where 姓名 = '%s'" % self.cust_name.text().strip())
                            while (self.query.next()):
                                if float(self.query.value(1)) - float(sum)<0:
                                    print(QMessageBox.critical(self, '警告',
                                                               '%商品可用余额不足\n可用余额为%s' % (name, self.query2.value(1)),
                                                               QMessageBox.Yes, QMessageBox.Yes))
                                    break
                                else:
                                    jifen = float(self.query.value(0)) + float(sum)
                                    keyongThing = float(self.query.value(1)) - float(sum)
                                    print("药品%s-%s=%s" % (float(self.query.value(1)), float(sum),float(self.query.value(1)) - float(sum)))
                                    kucunshuliang = self.query2.value(0)
                                    print("库存数量",kucunshuliang)
                                    flag = True

                if flag :
                    self.query.exec_("update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'"
                                 % (jifen, keyongThing, self.cust_name.text().strip()))
                    text = "update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'"% (jifen, keyongThing, self.cust_name.text().strip())
                    logging.info(text)
                    print(text)
                    #self.query.exec_("update 员工 set 时间 = '%s',记录='%s',金额='%s' where 工号 ='%s'"% (now, log, fin,self.))
                    #更改用户剩余手法次数

                    #更改商品信息
                    self.query2.exec_("update things set 库存数量 = '%s' where 名称 ='%s'"
                                      % (float(kucunshuliang) - di[name], name))
                    text = "update things set 库存数量 = '%s' where 名称 ='%s'"% (float(kucunshuliang) - di[name], name)
                    logging.info(text)

                if flag2:
                    for temp in Hand_FinList:
                        self.query.exec_("update 顾客 set %s = '%s' where 姓名 ='%s' or 电话='%s'"
                                         % (temp[0],temp[1],self.cust_name.text().strip(),self.cust_phone.text().strip()))
                        logging.info("update 顾客 set %s = '%s' where 姓名 ='%s'"%(temp[0],temp[1],self.cust_name.text()))

                    #print(self.cust_name.text().strip(),self.cust_phone.text().strip(),log, sum,keyongThing,Hand_FinList)

               # print("loks",log,Hand_FinList)
                if flag or flag2:
                    # 提交到log数据表
                    if self.cust_name.text().strip():
                        self.query.exec_(
                            'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")'
                            % (self.cust_name.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum))
                        text = 'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")' % (
                            self.cust_name.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum)

                        logging.info(text)
                    elif self.cust_phone.text().strip():
                        self.query.exec_('insert into log(电话,购买记录,购买时间,工号,金额)values("%s","%s","%s","%s","%s")'
                                         % (
                                             self.cust_phone.text().strip(), logtemp, now,
                                             self.lineEdit_2.text().strip(),
                                             sum))
                        text = "insert into log(电话,购买记录,购买时间,工号,金额) values('%s','%s','%s','%s','%s')" % (
                            self.cust_phone.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum)
                        logging.info(text)
                    #Printmain(self.cust_name.text().strip(),self.cust_phone.text().strip(),log, sum,keyongThing,Hand_FinList)  # 打印小票信息
                self.showShoufa.clear()
                self.showYaopin.clear()
                self.db.close()
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