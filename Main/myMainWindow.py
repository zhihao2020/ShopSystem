from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
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
from Addjifen import AddJifenData
from addpeopleNum import addShouNum
import datetime
import logging
import sqlite3
from connectPrinter import Printmain

logging.basicConfig(filename='ProgramLog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s:')


class reload_mainWin(QMainWindow, Ui_mainWindow):

    def __init__(self):
        super(reload_mainWin, self).__init__()
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
        self.action_6.triggered.connect(self.add_Jifen)
        self.action.triggered.connect(self.about)
        # 按钮
        self.pushButton_2.clicked.connect(self.jiesuan)
        self.pushButton.clicked.connect(self.init_find)
        # 触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        # 初始化
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
                tempText += "姓名:%s ,电话:%s ,生日:%s\n" % (self.query.value(0), self.query.value(1), self.query.value(2))
        if tempText != "":
            mixer.init()
            mixer.music.load(r"images\生日歌.mp3")
            mixer.music.play(loops=1, start=0.0)
            mixer.music.set_volume(1)
            QMessageBox.information(self, "提示", tempText, QMessageBox.Yes)

        self.db.close()

    def currentTab(self, index):
        if index == 0:
            self.index = 0
        elif index == 1:
            self.index = 1

    def init_find(self):
        self.find_Thing(self.thing_name.text().strip())

    def find_Thing(self, name):
        # 因为这是linetext changed触发的，所以此处加上异常处理
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

        # 刷新TabWidget

    def reFreash(self):
        # 重新刷新
        self.ThingsList = []
        self.handList = []
        self.showThings()
        self.showThings2()
        self.connect_LCD()

    def get_Row(self, kind):
        n = 0
        self.query.exec_("SELECT 名称 from things where 类别='{}'".format(kind))
        while (self.query.next()):
            n += 1
        # print("数据库中有",n,"行")
        return n

    def showThings(self):
        # 目标是商品的数据库
        self.openDB()
        self.showYaopin.setColumnCount(6)
        self.showYaopin.setRowCount(self.get_Row('商品'))
        self.showYaopin.setColumnWidth(0, 50)
        self.showYaopin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showYaopin.setHorizontalHeaderLabels(["", "名称", "单价", "备注", "库存数量", "数量"])
        self.showYaopin.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格自适应
        self.showYaopin.itemDoubleClicked.connect(self.changPrize)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='商品'")
        while (self.query.next()):
            # print("商品名称",self.query.value(0))
            self.ThingsList.append(self.query.value(0))
            self.query2.exec_("SELECT 名称,价格,备注,库存数量 from things where 名称='%s'" % self.query.value(0))
            # print("SELECT 名称,价格,备注 from things where 名称='%s'"%self.query.value(0))
            while (self.query2.next()):
                for n in range(4):
                    # print("第",i,"行，","第",n,"列")
                    ck = QCheckBox()
                    ck.setStyleSheet("QCheckBox::indicator { width: 35px; height: 35px;}")
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    # print(self.query2.value(n))
                    self.showYaopin.setCellWidget(i, 0, ck)
                    self.showYaopin.setItem(i, n + 1, newItem)
                    self.showYaopin.setCellWidget(i, 5, Qs)
            i += 1
        self.showYaopin.show()
        self.db.close()

    def showThings2(self):
        # 目标是手法的数据库
        self.openDB()
        self.showShoufa.setColumnCount(6)
        self.showShoufa.setRowCount(self.get_Row('手法'))
        self.showShoufa.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.showShoufa.setHorizontalHeaderLabels(["", "名称", "非会员价格", "备注", "剩余次数", "次数"])
        self.showShoufa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格自适应
        
        # self.showShoufa.itemDoubleClicked.connect(self.changPrize)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='手法'")
        while (self.query.next()):
            print("手法名称", self.query.value(0))
            self.handList.append(self.query.value(0))  # 保存手法的名录
            self.query2.exec_("SELECT 名称,价格,备注 from things where 名称='%s'" % self.query.value(0))
            while (self.query2.next()):
                for n in range(3):
                    # print("第", i, "行，", "第", n, "列")
                    ck = QCheckBox()
                    ck.setStyleSheet("QCheckBox::indicator { width: 35px; height: 35px;}")
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    print(self.query2.value(n))
                    self.showShoufa.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i, n + 1, newItem)
                    self.query3.exec_(
                        "SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text().strip()))
                    # print("SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text()))
                    while (self.query3.next()):
                        self.showShoufa.setItem(i, 4, QTableWidgetItem(str(self.query3.value(0))))
                    self.showShoufa.setCellWidget(i, 5, Qs)
            i += 1
        self.showShoufa.show()
        self.db.close()

    def changPrize(self, item):
        # print(222)
        if self.index == 0:
            # print(12,self.showYaopin.item(item.row(),1).text())
            self.change_Pice = ChangePrice(self.showYaopin.item(item.row(), 1).text(),
                                           self.showYaopin.item(item.row(), 2).text(), item.row())
            self.change_Pice.Signal_TwoParameter.connect(self.changePrize2)
            self.change_Pice.setWindowModality(Qt.ApplicationModal)
            self.change_Pice.show()
        else:
            self.change_Pice = ChangePrice(self.showShoufa.item(item.row(), 1).text(),
                                           self.showShoufa.item(item.row(), 2).text(), item.row())
            self.change_Pice.Signal_TwoParameter.connect(self.changePrize2)
            self.change_Pice.setWindowModality(Qt.ApplicationModal)
            self.change_Pice.show()

    def changePrize2(self, li):
        if self.index == 0:
            self.showYaopin.setItem(li[1], 2, QTableWidgetItem(li[0]))
        elif self.index == 1:
            self.showShoufa.setItem(li[1], 2, QTableWidgetItem(li[0]))

    def addInformation(self):
        self.addThingForm = addThing()
        self.addThingForm.Signal_FivesParameter.connect(self.addThing)
        self.addThingForm.setWindowModality(Qt.ApplicationModal)
        self.addThingForm.show()

    def addThing(self, lis):
        # [name,kind,price,num,beizhu]
        try:
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()

            print(self.ThingsList)
            if lis[0] in self.handList or lis[0] in self.ThingsList:
                reply = QMessageBox.critical(self, '警告', '将对该商品修改', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("select 库存数量 from things where 名称='%s'" % lis[0])
                    tempList = cursor.fetchall()
                    for n in tempList:
                        num = float(n[0]) + float(lis[3])
                        if lis[2]:
                            reply = QMessageBox.information(self,"提示","修改产品:%s\n修改价格为 %s\n修改库存数量为 %s"%(lis[0],lis[2],num),QMessageBox.Yes|QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                cursor.execute("update things set 价格='%s',库存数量='%s' where 名称='%s'" % (lis[2], num, lis[0]))
                                text = "update things set 价格='%s',库存数量='%s' where 名称='%s'" % (lis[2], num, lis[0])
                                logging.info('修改商品----%s' % text)
                                conn.commit()
                        else:
                            cursor.execute("update things set 库存数量='%s' where 名称='%s'" % (num, lis[0]))
                            text = "update things set 库存数量='%s' where 名称='%s'" % (num, lis[0])
                            logging.info('修改商品----%s' % text)
                            conn.commit()
            else:
                if lis[1] == "手法":
                    reply = QMessageBox.information(self, "提示", '将要添加手法', QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        try:
                            cursor.execute("insert into things(名称,类别,价格,备注) values('%s','%s','%s','%s')" % (
                                lis[0], lis[1], lis[2], lis[4]))
                            cursor.execute("alter table 顾客 add %s int;" % (lis[0]))
                            text = "alter table 顾客 add %s int;" % (lis[0])
                            print(text)
                            conn.commit()
                        except:
                            print(QMessageBox.critical(self, "警告", '添加错误\n错误代码:4543', QMessageBox.Yes))
                        else:
                            print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes))
                            logging.info('添加商品----%s' % text)
                else:
                    reply = QMessageBox.information(self, "提示", '将要添加商品', QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        try:
                            cursor.execute("insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (
                            lis[0], lis[1], lis[2], lis[3], lis[4]))
                            text = "insert into things(名称,类别,价格,库存数量,备注) values('%s','%s','%s','%s','%s')" % (
                            lis[0], lis[1], lis[2], lis[3], lis[4])
                            conn.commit()
                        except:
                            print(QMessageBox.critical(self, "警告", '添加错误\n错误代码:4544', QMessageBox.Yes))
                        else:
                            print(QMessageBox.information(self, "提示", '添加成功', QMessageBox.Yes))
                            logging.info('添加商品----%s' % text)
        finally:
            conn.close()

    def addPeople_init(self):
        self.addPeopleForm = addPeople()
        self.addPeopleForm.Signal_FourParameter.connect(self.addPeople)
        self.addPeopleForm.setWindowModality(Qt.ApplicationModal)
        self.addPeopleForm.show()

    def addPeople(self, lis):
        # [name,year,dianhua]
        name = []
        phone = []
        try:
            uidNum = 0
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            cursor.execute("select 姓名,电话 from 顾客")

            for tempNum in cursor.fetchall():
                name.append(tempNum[0])
                phone.append(tempNum[1])
                uidNum += 1

            if lis[0] in name or lis[1] in phone:
                QMessageBox.information(self, '提示', '该用户已经存在', QMessageBox.Yes)
                raise Exception("用户已存在")
            else:
                reply = QMessageBox.information(self, '提示', '将添加新用户\n 仅仅添加姓名:%s、年龄:%s、电话信息:%s' % (lis[0], lis[1], lis[2]),
                                                QMessageBox.Yes | QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("insert into 顾客(uid,姓名,年龄,电话,生日) values('%d','%s','%s','%s','%s')" % (
                    uidNum, lis[0], lis[1], lis[2], lis[3]))
                    conn.commit()
        except IOError:
            QMessageBox.critical(self,"警告","请检查数据库文件\n或与管理员联系\n错误代码：8689",QMessageBox.Yes)
            conn.rollback()
        except Exception as e:
            if e =="用户已存在":
                pass
            else:
                QMessageBox.critical(self,"警告","请与管理员联系\n错误代码：8690",QMessageBox.Y)
                conn.rollback()
        else:
            print(QMessageBox.information(self, "提示", '添加用户成功', QMessageBox.Yes | QMessageBox.Yes))
            text = "insert into 顾客(uid,姓名,年龄,电话,生日) values('%d','%s','%s','%s','%s')" % (
                uidNum, lis[0], lis[1], lis[2], lis[3])
            logging.info('添加用户---%s' % text)
        finally:
            conn.close()


    def init_addUserMoney(self):
        self.addPeopleMoney = addMoney()
        self.addPeopleMoney.Signal_ThreeParameter.connect(self.addUserMoney)
        self.addPeopleMoney.setWindowModality(Qt.ApplicationModal)
        self.addPeopleMoney.show()

    def addUserMoney(self, lis):
        self.addPeopleMoney.setWindowModality(Qt.ApplicationModal)
        self.addPeopleMoney.show()
        try:
            name = []
            phone = []
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            cursor.execute("select 姓名,电话 from 顾客")
            for tempNum in cursor.fetchall():
                name.append(tempNum[0])
                phone.append(tempNum[1])

            if lis[0] in name:
                reply = QMessageBox.information(self, '提示', '将对该用户%s进行充值' % lis[0], QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("SELECT 药品可用金额 from 顾客 where 姓名 ='%s'" % lis[0])

                    shangpin = float(cursor.fetchone()[0]) + float(lis[2])
                    with sqlite3.connect("data/all.db") as tempdata:
                        tempdata.execute("update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin, lis[0]))
                        text = "update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin, lis[0])
                        logging.info('用户修改---%s' % text)

            elif lis[1] in phone:
                reply = QMessageBox.information(self, '提示', '将对该用户%s 进行充值' % lis[1], QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("SELECT 药品可用金额 from 顾客 where 电话 ='%s'" % lis[1])
                    shangpin = float(cursor.fetchone()[0]) + float(lis[2])
                    with sqlite3.connect("data/all.db") as tempdata:
                        tempdata.execute("update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin, lis[1]))
                        text = "update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin, lis[1])
                        logging.info('用户修改---%s' % text)
            else:
                QMessageBox.information(self, '提示', '不存在该用户', QMessageBox.Yes | QMessageBox.Yes)
        except IOError:
            QMessageBox.critical(self, "警告", "请检查数据库文件\n或与管理员联系\n错误代码:4401", QMessageBox.Yes)
        except sqlite3.OperationalError:
            QMessageBox.critical(self, "警告", "数据库被锁定\n请检查姓名或电话的唯一性\n错误代码:4402", QMessageBox.Yes)
        finally:
            conn.close()

    def init_addUserShouNum(self):
        self.addPeopleShouNum = addShouNum(self.handList)
        self.addPeopleShouNum.Signal_FourParameter.connect(self.addUserShouNum)
        self.addPeopleShouNum.setWindowModality(Qt.ApplicationModal)
        self.addPeopleShouNum.show()

    def addUserShouNum(self, lis):
        try:
            name = []
            phone = []
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            cursor.execute("select 姓名,电话 from 顾客")
            for tempNum in cursor.fetchall():
                name.append(tempNum[0])
                phone.append(tempNum[1])

            if lis[0] in name:

                reply = QMessageBox.information(self, '提示', '对用户:%s\n充值%s'%(lis[0],lis[2]), QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("select %s from 顾客 where 姓名='%s' " % (lis[2], lis[0]))
                    initNum = cursor.fetchone()[0]
                    if not initNum:
                        initNum = 0

                    Num = initNum + int(lis[3])
                    cursor.execute("update 顾客 set %s='%s' where 姓名='%s'" % (lis[2], Num, lis[0]))
                    conn.commit()
                    text = "update 顾客 set %s='%s' where 姓名='%s'" % (lis[2], Num, lis[0])
                    print(text)
            elif lis[1] in phone:
                reply = QMessageBox.information(self, '提示', '对用户 %s\n充值:%s'%(lis[1],lis[2]), QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("select %s from 顾客 where 电话='%s' " % (lis[2], lis[1]))
                    initNum = cursor.fetchone()[0]

                    if not initNum:
                        initNum = 0

                    Num = initNum + int(lis[3])
                    cursor.execute("update 顾客 set %s='%s' where 电话='%s'" % (lis[2], Num, lis[1]))
                    conn.commit()
                    text = "update 顾客 set %s='%s' where 电话='%s'" % (lis[2], Num, lis[1])
                    print(text)
            else:
                QMessageBox.information(self, '提示', '该用户不存在', QMessageBox.Yes)
        except sqlite3.ProgrammingError:
            QMessageBox.critical(self,"警告","表未找到或SQL 语句存在语法错误\n请联系管理员\n错误代码:2345",QMessageBox.Yes)
            conn.rollback()
        except sqlite3.OperationalError:
            QMessageBox.critical(self, "警告", "数据库操作失败\n请联系管理员\n错误代码:2346", QMessageBox.Yes)
            conn.rollback()

        else:
            logging.info('用户修改---%s' % text)
        finally:
            conn.close()

    def lookCust(self):
        self.lookCust_Data = lookCustData()
        self.lookCust_Data.show()

    def connect_LCD(self):
        self.openDB()
        try:
            if self.cust_name.text().strip():
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 姓名 = '%s'" % (self.cust_name.text().strip())
            else:
                MONERY = "SELECT 药品可用金额,积分 from 顾客 where 电话=%s" % (self.cust_phone.text().strip())
            self.query.exec_(MONERY)
            while (self.query.next()):
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
        log = []  # 购买记录
        logtemp = []
        Hand_FinList = []
        keyongThing = None
        jifen = 0
        i = 0
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        if not self.cust_name.text().strip() and not self.cust_phone.text().strip():
            print(QMessageBox.information(self, '提示', '进入非会员模式', QMessageBox.Yes, QMessageBox.Yes))
            while (i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append(
                    [self.showYaopin.cellWidget(i, 0), '商品', self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                     self.showYaopin.cellWidget(i, 5)])
                i += 1
            for line in lines:
                # 复选框、类别、名称、价格、数量
                if line[0].checkState() == Qt.Checked:
                    if line[1] == '商品':
                        sum_Things += float(line[3].text()) * float(line[4].value())

                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典
                    logtemp.append([line[2].text(), line[4].value()]) # 名称 单价 数量
                    log.append([line[2].text(), line[3].text(), line[4].value()])  # 购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
            fin = sum_Things
            reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                for name in di.keys():
                    self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                    while (self.query2.next()):
                        if (float(self.query2.value(0)) - di[name] < 0):
                            print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                        else:
                            kucunshuliang = self.query2.value(0)
                            flag = True
                            logging.info("%s消费 %s" % (self.cust_name.text().strip, fin))
                if flag:
                    # self.query.exec_("update 员工 set 时间 = '%s',记录='%s',金额='%s' where 工号 ='%s'"% (now, log, fin,self.))
                    # 更改商品信息
                    self.query2.exec_(
                        "update things set 库存数量 = '%s' where 名称 ='%s'" % (float(kucunshuliang) - di[name], name))
                    text = "update things set 库存数量 = '%s' where 名称 ='%s'" % (float(kucunshuliang) - di[name], name)
                    logging.info(text)
                    # 提交到log数据表
                    Printmain(log, fin)  # 打印小票信息

        elif self.lineEdit_2.text():
            i = 0
            while (i < self.showYaopin.rowCount()):
                # 复选框、类别、名称、价格、数量
                lines.append(
                    [self.showYaopin.cellWidget(i, 0), '商品', self.showYaopin.item(i, 1), self.showYaopin.item(i, 2),
                     self.showYaopin.cellWidget(i, 5)])
                i += 1
            i = 0
            while (i < self.showShoufa.rowCount()):
                lines.append([self.showShoufa.cellWidget(i, 0), '手法', self.showShoufa.item(i, 1),
                              self.showShoufa.item(i, 4), self.showShoufa.cellWidget(i, 5)])
                # print(self.showShoufa.item(i, 4).text())
                i += 1
            for line in lines:
                # 复选框、类别、名称、使用次数、剩余数量
                if line[0].checkState() == Qt.Checked:
                    if line[1] == '手法':
                        # 复选框、类别、名称、次数、剩余次数
                        HandList.append(line)

                    if line[1] == '商品':
                        sum_Things += float(line[3].text()) * float(line[4].value())
                        log.append([line[2].text(), line[3].text(), line[4].value()])  # 购买记录[[a,b,a],[c,d,v]] 名称、价格、数量
                    logtemp.append([line[2].text(), line[4].value()])
                    di[line[2].text()] = float(line[4].value())  # 加入已选的名称和数量 构成字典

                    sum = sum_Things

            reply = QMessageBox.information(self, '提示', '商品消费金额%s' % sum, QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                try:
                    for Hand_num in HandList:
                        # 复选框、类别、名称、次数、剩余次数
                        if int(Hand_num[3].text()) - int(Hand_num[4].value()) < 0:

                            print(QMessageBox.information(self, '提示', '%s剩余次数不足' % Hand_num[2].text(), QMessageBox.Yes,
                                                          QMessageBox.Yes))
                            raise Exception("剩余次数不足")
                        elif int(Hand_num[3].text()) == 0:
                            print(QMessageBox.information(self, '提示', '%s 次数不足' % Hand_num[2].text(), QMessageBox.Yes,
                                                          QMessageBox.Yes))
                            raise Exception("次数不足")
                        else:
                            Rest_num = int(Hand_num[3].text()) - int(Hand_num[4].value())
                            Hand_FinList.append([Hand_num[2].text(), Rest_num, int(Hand_num[4].value())])  # 名称、数量
                            flag2 = True

                    for name in di.keys():
                        if self.cust_name.text().strip():
                            self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                            while (self.query2.next()):
                                if not self.query2.value(0):
                                    print("没有数量")
                                    break
                                elif float(self.query2.value(0)) - di[name] < 0:
                                    print(QMessageBox.critical(self, '警告', '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                                    raise Exception("商品库存不足")
                                else:
                                    self.query.exec_("SELECT 积分,药品可用金额 from 顾客 where 姓名 = '%s'" % self.cust_name.text().strip())
                                    while (self.query.next()):
                                        if float(self.query.value(1)) - float(sum) < 0:
                                            print(QMessageBox.critical(self, '警告',
                                                                       '%商品可用余额不足\n可用余额为%s' % (name, self.query2.value(1)),
                                                                       QMessageBox.Yes, QMessageBox.Yes))
                                            raise Exception("商品余额不足")
                                        else:
                                            jifen = float(self.query.value(0)) + float(sum)
                                            keyongThing = float(self.query.value(1)) - float(sum)
                                            print("药品%s-%s=%s" % (float(self.query.value(1)), float(sum), float(self.query.value(1)) - float(sum)))
                                            kucunshuliang = self.query2.value(0)
                                            flag = True
                        else:
                            self.query2.exec_("SELECT 库存数量 from things where 名称='%s'" % name)
                            while (self.query2.next()):
                                if not self.query2.value(0):
                                    print("没有数量")
                                    break
                                elif float(self.query2.value(0)) - di[name] < 0:
                                    print(QMessageBox.critical(self, '警告',
                                                               '%s商品库存不足\n现有库存%s' % (name, self.query2.value(0)),
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                                    raise Exception("商品库存不足")
                                else:
                                    self.query.exec_(
                                        "SELECT 积分,药品可用金额 from 顾客 where 电话 = '%s'" % self.cust_phone.text().strip())
                                    while (self.query.next()):
                                        if float(self.query.value(1)) - float(sum) < 0:
                                            print(QMessageBox.critical(self, '警告',
                                                                       '%商品可用余额不足\n可用余额为%s' % (name, self.query2.value(1)),
                                                                       QMessageBox.Yes, QMessageBox.Yes))
                                            raise Exception("商品余额不足")
                                        else:
                                            jifen = float(self.query.value(0)) + float(sum)
                                            keyongThing = float(self.query.value(1)) - float(sum)
                                            print("药品%s-%s=%s" % (float(self.query.value(1)), float(sum),
                                                                  float(self.query.value(1)) - float(sum)))
                                            kucunshuliang = self.query2.value(0)
                                            flag = True
                except AttributeError:
                    QMessageBox.critical(self,"提示","请摁F4刷新界面，重新处理订单",QMessageBox.Yes)
                except Exception as e:
                    logging.warning(e)
                self.db.close()
                #获取uid 并 改进 log
                try:
                    logging.info("-----进入结算------")
                    conn = sqlite3.connect("data/all.db")
                    cursor = conn.cursor()

                    if flag:
                        if self.cust_name.text().strip():
                            cursor.execute("update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'"
                                             % (jifen, keyongThing, self.cust_name.text().strip()))
                            text1 = "update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'" % (
                            jifen, keyongThing, self.cust_name.text().strip())

                            logging.info(text1)
                            # 更改商品信息
                            cursor.execute("update things set 库存数量 = '%s' where 名称 ='%s'"
                                              % (float(kucunshuliang) - di[name], name))
                            conn.commit()
                            text2 = "update things set 库存数量 = '%s' where 名称 ='%s'" % (float(kucunshuliang) - di[name], name)
                            logging.info(text2)
                        else:
                            cursor.execute("update 顾客 set 积分 = '%s',药品可用金额='%s' where 电话 ='%s'"
                                           % (jifen, keyongThing, self.cust_phone.text().strip()))
                            text1 = "update 顾客 set 积分 = '%s',药品可用金额='%s' where 电话 ='%s'" % (
                                jifen, keyongThing, self.cust_phone.text().strip())

                            logging.info(text1)
                            # 更改商品信息
                            cursor.execute("update things set 库存数量 = '%s' where 名称 ='%s'"
                                           % (float(kucunshuliang) - di[name], name))
                            conn.commit()
                            text2 = "update things set 库存数量 = '%s' where 名称 ='%s'" % (
                            float(kucunshuliang) - di[name], name)
                            logging.info(text2)

                    elif flag2:
                        if self.cust_name.text().strip():
                            for temp in Hand_FinList:
                                print(temp)
                                text3 = "update 顾客 set %s = '%s' where 姓名 ='%s'" % (temp[0], temp[1], self.cust_name.text())
                                print(text3)
                                cursor.execute("update 顾客 set %s = '%s' where 姓名 ='%s'"% (temp[0], temp[1],self.cust_name.text()))
                                text3 = "update 顾客 set %s = '%s' where 姓名 ='%s'" % (temp[0], temp[1], self.cust_name.text())
                                logging.info(text3)
                            conn.commit()
                        else:
                            for temp in Hand_FinList:
                                print(temp)
                                text3 = "update 顾客 set %s = '%s' where 电话 ='%s'" % (
                                temp[0], temp[1], self.cust_phone.text())
                                print(text3)
                                cursor.execute("update 顾客 set %s = '%s' where 电话 ='%s'" % (
                                temp[0], temp[1], self.cust_phone.text()))
                                text3 = "update 顾客 set %s = '%s' where 电话 ='%s'" % (
                                temp[0], temp[1], self.cust_phone.text())
                                logging.info(text3)
                            conn.commit()


                    elif flag or flag2:
                        # 提交到log数据表
                        if self.cust_name.text().strip():
                            cursor.execute(
                                'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")'
                                % (self.cust_name.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum))
                            #conn.commit()
                            text4 = 'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")' % (
                                self.cust_name.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum)
                            logging.info(text4)
                        elif self.cust_phone.text().strip():
                            cursor.execute('insert into log(电话,购买记录,购买时间,工号,金额)values("%s","%s","%s","%s","%s")'
                                             % (
                                                 self.cust_phone.text().strip(), logtemp, now,
                                                 self.lineEdit_2.text().strip(),
                                                 sum))
                            conn.commit()
                            text5 = "insert into log(电话,购买记录,购买时间,工号,金额) values('%s','%s','%s','%s','%s')" % (
                                self.cust_phone.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sum)
                            logging.info(text5)
                        print(self.cust_name.text().strip(), self.cust_phone.text().strip(), log, sum, keyongThing,Hand_FinList)
                        Printmain(self.cust_name.text().strip(), self.cust_phone.text().strip(), log, sum, keyongThing,Hand_FinList)  # 打印小票信息

                    else:
                        QMessageBox.warning(self,"提醒","未进入结算环节\n请检查用户姓名或电话号码",QMessageBox.Yes)
                except IOError:
                    QMessageBox.critical(self,"警告","检查数据库连接\n并与管理员联系\n错误代码:3456",QMessageBox.Yes)
                    conn.rollback()
                    logging.info("-----以上消息失效------")
                except sqlite3.OperationalError:
                    QMessageBox.critical(self, "警告", "数据库操作失败\n并与管理员联系\n错误代码:3457",QMessageBox.Yes)
                    conn.rollback()
                    logging.info("-----以上消息失效------")
                except UnboundLocalError:
                    QMessageBox.critical(self, "警告", "检查打印机连接\n或与管理员联系\n错误代码:3458",QMessageBox.Yes)
                    conn.rollback()
                    logging.info("-----以上消息失效------")
                except:
                    QMessageBox.critical(self, "警告", "错误代码:3459\n请与管理员联系",QMessageBox.Yes)
                    conn.rollback()
                    logging.info("-----以上消息失效------")

                finally:
                    conn.close()
                    #初始化
                    self.cust_name.setText("")
                    self.cust_phone.setText("")
                    self.showShoufa.clear()
                    self.showYaopin.clear()

        else:
            print(QMessageBox.information(self, '提示', '请输入员工工号', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes))

    def add_Jifen(self):
        self.add_Jifen_temp = AddJifenData()
        self.add_Jifen_temp.show()
    # 关闭数据库
    def closeEvent(self, event):
        self.db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())
