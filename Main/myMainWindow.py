from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5 import QtCore,QtGui
import sys
import webbrowser
import json
from pygame import mixer
import datetime
import time
import smtplib
from email.mime.text import MIMEText
import logging
import sqlite3
import os
import requests
import pyautogui
import subprocess
from configparser import ConfigParser
import zipfile
from UI.MainWindow import Ui_mainWindow
from Addpeople import addPeople
from Addthing import addThing
from AddpeopleMoney import addMoney
from ChangeZhekou import ChangePrice
from customerData import DataGrid
from Addjifen import AddJifenData
from addpeopleNum import addShouNum
from SpendMoney import SpendWindow
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
        self.clock_beifen()
        self.trayIcon()
        self.wenzitishi = Information()

        self.thread = Thread()
        self.thread.sleep_signal.connect(self.windowSleep)
        self.thread.information_signal.connect(self.showInformation)
        self.thread.start()
        QApplication.setQuitOnLastWindowClosed(False)
        self.update_thread = update_Thread()
        self.update_thread.update_Signal.connect(self.update_soft)
        if datetime.datetime.now().weekday() == 3:
            self.update_thread.start()
    def init(self):
        self.cfg = ConfigParser()
        self.cfg.read("config.ini")
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
        self.action_9.triggered.connect(self.update_soft)
        self.action_10.triggered.connect(self.beifen)
        self.action_11.triggered.connect(self.publish_previous)
        self.action_12.triggered.connect(self.init_spendmoney)
        self.action.triggered.connect(self.about)
        # 按钮
        self.pushButton_2.clicked.connect(self.Flow)
        self.pushButton.clicked.connect(self.init_find)
        # 触发LCD
        self.cust_name.textChanged.connect(self.connect_LCD)
        self.cust_phone.textChanged.connect(self.connect_LCD)
        # 初始化
        self.showThings()
        self.showThings2()
        self.tabWidget.currentChanged['int'].connect(self.currentTab)
        self.index = 0

    def showInformation(self,flag):
        if flag:
            self.wenzitishi.show()
        else:
            if self.wenzitishi.isVisible():
                self.wenzitishi.close()

    def windowSleep(self,flag):
        if flag:
            sys.exit(1)

    def update_soft(self,up_soft):
        if up_soft:
            reply = QMessageBox.information(self,"提示","有新版软件，是否更新？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.beifen():
                    #运行update.exe
                    subprocess.call("update.exe",shell=True)
                else:QMessageBox.information(self,"提示","备份失败",QMessageBox.Yes)
        else:
            with open('update.ini','w') as f:
                f.write("%s,%s,%s"%('','',0))
            reply = QMessageBox.information(self, "提示", "是否检查更新？", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.beifen():
                    # 运行update.exe
                    subprocess.call("update.exe", shell=True)
                else:
                    QMessageBox.information(self, "提示", "备份失败", QMessageBox.Yes)

    def clock_beifen(self):
        if datetime.datetime.now().weekday() == 4:
            self.beifen()

    def beifen(self):
        try:
            dir = r"C:\YIQIguanli"
            file = r"C:\YIQIguanli\%s.zip"%time.strftime("%Y-%m-%d", time.localtime())
            if not os.path.exists(dir):
                os.makedirs(dir)
            newZip = zipfile.ZipFile(file,'w')
            newZip.write('data/all.db')
            newZip.write('data/password.db')
            newZip.write("ProgramLog.log")
            newZip.close()
        except:
            QMessageBox.warning(self,"警告","备份过程发生错误",QMessageBox.Yes)
        else:
            QMessageBox.information(self,"提示","备份完成，请定时备份数据文件",QMessageBox.Yes)
            logging.info('备份数据文件')
            return True

    def trayIcon(self):
        tuopan = QSystemTrayIcon(self)
        tuopan.setIcon(QtGui.QIcon(r"images/snail.ico"))
        tuopan.setToolTip(u"欢迎使用医琦软件")
        a1 = QAction('&显示(Show)',self,triggered=self.showNormal)
        a2 = QAction('&退出(Exit)',self,triggered=self.quit_app)  # 直接退出可以用qApp.quit
        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        tuopan.setContextMenu(tpMenu)
        tuopan.activated.connect(self.iconActivated)
        tuopan.show()

    def iconActivated(self,reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isMinimized() or not self.isVisible():
                self.showNormal()
                self.activateWindow()
            else:
                self.hide()
        elif reason == QSystemTrayIcon.Trigger:
            pass

    def quit_app(self):
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            sys.exit(app.exec_())

    def openDB(self):
        self.db.open()
        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
            logging.error("数据库连接失败，请查看数据库配置")
        self.query = QSqlQuery(self.db)
        self.query2 = QSqlQuery(self.db)
        self.query3 = QSqlQuery(self.db)

    def about(self):
        webbrowser.open_new_tab('https://xuzhihao.top/about/')

    def birthDayMusic(self):
        self.openDB()
        tempText = ""
        self.query.exec_("SELECT 姓名,电话,生日 from 顾客 ")
        while (self.query.next()):
            if datetime.datetime.today().strftime('%m/%d') in self.query.value(2):
                tempText += "姓名:%s ,电话:%s ,生日:%s\n" % (self.query.value(0), self.query.value(1), self.query.value(2))
        if tempText != "":
            mixer.init()
            mixer.music.load(r"images\birthday.mp3")
            mixer.music.play(loops=1, start=0.0)
            mixer.music.set_volume(1)
            QMessageBox.information(self, "提示", tempText, QMessageBox.Yes)
        self.db.close()

    def publish_previous(self):
        with open("ppx.json","r",encoding="utf-8") as fd:
            s = json.load(fd)
            Printmain(name=s[0], phone =s[1], data=s[2], fin=s[3], keyongThing=s[4],Hand_FinList=s[5])  # 打印小票信息

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
                items = self.showShoufa.findItems(self.thing_name.text().strip(), QtCore.Qt.MatchContains)
                item = items[0]
                # 选中单元格
                item.setSelected(True)
                row = item.row()
                # 滚轮定位过去，快速定位
                self.showShoufa.verticalScrollBar().setSliderPosition(row)
            except:
                pass

    def reFreash(self):
        # 重新刷新
        self.ThingsList.clear()
        self.handList.clear()
        self.showThings()
        self.showThings2()
        self.connect_LCD()

    def get_Row(self, kind):
        n = 0
        self.query.exec_("SELECT 名称 from things where 类别='{}'".format(kind))
        while (self.query.next()):
            n += 1
        return n

    def showThings(self):
        # 目标是商品的数据库
        self.openDB()
        self.showYaopin.setColumnCount(6)
        self.showYaopin.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.showYaopin.setRowCount(self.get_Row('商品'))
        self.showYaopin.setColumnWidth(0, 50)
        self.showYaopin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.showYaopin.setHorizontalHeaderLabels(["", "名称", "单价", "备注", "库存数量", "数量"])
        self.showYaopin.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格自适应
        self.showYaopin.itemDoubleClicked.connect(self.changPrize)
        #self.showYaopin.resizeColumnsToContents()
        #self.showYaopin.resizeRowsToContents()#行高适应内容
        self.showYaopin.setSelectionBehavior(QAbstractItemView.SelectRows)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='商品'")
        while (self.query.next()):
            # print("商品名称",self.query.value(0))
            self.ThingsList.append(self.query.value(0))
            self.query2.exec_("SELECT 名称,价格,备注,库存数量 from things where 名称='%s'" % self.query.value(0))
            # print("SELECT 名称,价格,备注 from things where 名称='%s'"%self.query.value(0))
            while (self.query2.next()):
                for n in range(4):
                    ck = QCheckBox()
                    combox_Style="QCheckBox::indicator { width:32px; height: 32px;} " \
                                 "QCheckBox::indicator::unchecked {image: url(%s/images/unchecked.png);}" \
                                 "QCheckBox::indicator::checked {image: url(%s/images/checked.png);}"%(os.getcwd(),os.getcwd())
                    combox_Style = combox_Style.replace("\\","/")
                    ck.setStyleSheet(combox_Style)
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    newItem.setFont(QtGui.QFont("SimSun", 20))
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
       # self.showShoufa.resizeRowsToContents()  # 行高适应内容
        self.showShoufa.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.showShoufa.itemDoubleClicked.connect(self.changPrize)
        i = 0
        self.query.exec_("SELECT 名称 from things where 类别='手法'")
        while (self.query.next()):

            self.handList.append(self.query.value(0))  # 保存手法的名录
            self.query2.exec_("SELECT 名称,价格,备注 from things where 名称='%s'" % self.query.value(0))
            while (self.query2.next()):
                for n in range(3):
                    # print("第", i, "行，", "第", n, "列")
                    ck = QCheckBox()
                    combox_Style = "QCheckBox::indicator { width:32px; height: 32px;} " \
                                   "QCheckBox::indicator::unchecked {image: url(%s/images/unchecked.png);}" \
                                   "QCheckBox::indicator::checked {image: url(%s/images/checked.png);}" % (
                                   os.getcwd(), os.getcwd())
                    combox_Style = combox_Style.replace("\\", "/")
                    ck.setStyleSheet(combox_Style)
                    Qs = QSpinBox()
                    newItem = QTableWidgetItem(str(self.query2.value(n)))
                    newItem.setFont(QtGui.QFont("SimSun", 20))
                    self.showShoufa.setCellWidget(i, 0, ck)
                    self.showShoufa.setItem(i, n + 1, newItem)
                    if self.cust_name.text().strip() != "":
                        self.query3.exec_(
                            "SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text().strip()))
                    else:
                        self.query3.exec_(
                            "SELECT %s from 顾客 where 电话='%s'" % (self.query2.value(0), self.cust_phone.text().strip()))

                    self.showShoufa.setCellWidget(i, 5, Qs)
                    # print("SELECT %s from 顾客 where 姓名='%s'" % (self.query2.value(0), self.cust_name.text()))
                littleFlag = False
                while (self.query3.next()):
                    restItem =  QTableWidgetItem(str(self.query3.value(0)))
                    restItem.setFont(QtGui.QFont("SimSun", 20))
                    self.showShoufa.setItem(i, 4,restItem)
                    littleFlag = True
                if not littleFlag:
                    self.showShoufa.setItem(i, 4, QTableWidgetItem(" "))
            i += 1
        self.showShoufa.show()
        self.db.close()

    def changPrize(self, item):
        # print(222)
        if self.index == 0:
            #print(12,self.showYaopin.item(item.row(),1).text())
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
                            reply = QMessageBox.information(self, "提示",
                                                            "修改产品:%s\n修改价格为 %s\n修改库存数量为 %s" % (lis[0], lis[2], num),
                                                            QMessageBox.Yes | QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                cursor.execute(
                                    "update things set 价格='%s',库存数量='%s' where 名称='%s'" % (lis[2], num, lis[0]))
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
                            text = "alter table 顾客 add '%s' int" % (lis[0])
                            print(text)
                            cursor.execute("alter table 顾客 add '%s' int" % (lis[0]))
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
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            cursor.execute("select 姓名,电话 from 顾客")

            for tempNum in cursor.fetchall():
                name.append(tempNum[0])
                phone.append(tempNum[1])

            if lis[0] in name or lis[1] in phone:
                QMessageBox.information(self, '提示', '该用户已经存在', QMessageBox.Yes)
                raise Exception("用户已存在")
            else:
                reply = QMessageBox.information(self, '提示',
                                                '将添加新用户\n 仅仅添加姓名:%s、年龄:%s、电话信息:%s' % (lis[0], lis[1], lis[2]),
                                                QMessageBox.Yes | QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("insert into 顾客(姓名,年龄,电话,生日) values('%s','%s','%s','%s')" % (
                        lis[0], lis[1], lis[2], lis[3]))
                    conn.commit()
        except IOError:
            QMessageBox.critical(self, "警告", "请检查数据库文件\n或与管理员联系\n错误代码：8689", QMessageBox.Yes)
            conn.rollback()
        except Exception as e:
            if e == "用户已存在":
                pass
            else:
                QMessageBox.critical(self, "警告", "%s\n错误代码：8690"%e, QMessageBox.Yes)
                conn.rollback()
        else:
            print(QMessageBox.information(self, "提示", '添加用户成功', QMessageBox.Yes | QMessageBox.Yes))
            text = "insert into 顾客(姓名,年龄,电话,生日) values('%s','%s','%s','%s')" % (
                 lis[0], lis[1], lis[2], lis[3])
            logging.info('添加用户---%s' % text)
        finally:
            conn.close()

    def init_spendmoney(self):
        self.SpendWindow = SpendWindow()
        self.SpendWindow.Signal_TwoParameter.connect(self.spendmoney)
        self.SpendWindow.setWindowModality(Qt.ApplicationModal)
        self.SpendWindow.show()

    def spendmoney(self,lis):
        try:
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            cursor.execute("select 药品可用金额 from 顾客 where 姓名='%s' or 电话 ='%s'"%(lis[0],lis[0]))
            #print("select 药品可用金额 from 顾客 where 姓名='%s' or 电话='%s'"%(lis[0],lis[0]))
            tempList = cursor.fetchone()
            money = float(lis[1])+float(tempList[0]) #最后得到的金额
            if money >= 0:
                reply = QMessageBox.information(self, '提示', '将对该用户 %s 进行充值 %s' % (lis[0],lis[1]), QMessageBox.Yes,QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("update 顾客 set 药品可用金额=%s where 姓名='%s' or 电话 ='%s'" % (money,lis[0],lis[0]))
                    text = "update 顾客 set 药品可用金额=%s where 姓名='%s' or 电话 ='%s'" % (money,lis[0],lis[0])

                data = [['直接扣费','','%s'%lis[1],'1']]

                Printmain(name=lis[0], phone=lis[0], data=data, fin=lis[1], keyongThing=money)  # 打印小票信息
                reply = QMessageBox.information(self, "提示", "是否继续打印小票？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    publish_previous_list = [lis[0],lis[0], data, lis[1], money,None]
                    with open("ppx.json", "w", encoding="utf-8") as fd:
                        fd.write(json.dumps(publish_previous_list))
                    Printmain(name=lis[0], phone=lis[0], data=data, fin=lis[1], keyongThing=money)  # 打印小票信息
            else:
                QMessageBox.information(self,"提示","用户 %s 剩余金额不足"%lis[0],QMessageBox.Yes)
        except IOError:
            QMessageBox.critical(self, "警告", "请检查数据库文件\n或与管理员联系\n错误代码:4501", QMessageBox.Yes)
        except Exception as e:
            QMessageBox.critical(self, "警告", "%s\n错误代码:4502"%e, QMessageBox.Yes)
        else:
            logging.info('【用户消费】---%s' % text)
            conn.commit()
        finally:
            conn.close()

    def init_addUserMoney(self):
        self.addPeopleMoney = addMoney()
        self.addPeopleMoney.Signal_ThreeParameter.connect(self.addUserMoney)
        self.addPeopleMoney.setWindowModality(Qt.ApplicationModal)
        self.addPeopleMoney.show()

    def addUserMoney(self, lis):
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
                reply = QMessageBox.information(self, '提示', '将对该用户%s进行充值' % lis[0], QMessageBox.Yes,QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("SELECT 药品可用金额 from 顾客 where 姓名 ='%s'" % lis[0])

                    shangpin = float(cursor.fetchone()[0]) + float(lis[2])
                    with sqlite3.connect("data/all.db") as tempdata:
                        tempdata.execute("update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin, lis[0]))
                        text = "update 顾客 set 药品可用金额=%s where 姓名='%s'" % (shangpin, lis[0])

            elif lis[1] in phone:
                reply = QMessageBox.information(self, '提示', '将对该用户%s 进行充值' % lis[1], QMessageBox.Yes,QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("SELECT 药品可用金额 from 顾客 where 电话 ='%s'" % lis[1])
                    shangpin = float(cursor.fetchone()[0]) + float(lis[2])
                    with sqlite3.connect("data/all.db") as tempdata:
                        tempdata.execute("update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin, lis[1]))
                        text = "update 顾客 set 药品可用金额='%s' where 电话='%s'" % (shangpin, lis[1])
            else:
                QMessageBox.information(self, '提示', '不存在该用户', QMessageBox.Yes | QMessageBox.Yes)
        except IOError:
            QMessageBox.critical(self, "警告", "请检查数据库文件\n或与管理员联系\n错误代码:4401", QMessageBox.Yes)
        except sqlite3.OperationalError:
            QMessageBox.critical(self, "警告", "数据库被锁定\n请检查姓名或电话的唯一性\n错误代码:4402", QMessageBox.Yes)
        else:
            conn.commit()
            logging.info('用户修改---%s' % text)
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

                reply = QMessageBox.information(self, '提示', '对用户:%s\n充值%s' % (lis[0], lis[2]), QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("select %s from 顾客 where 姓名='%s' " % (lis[2], lis[0]))
                    initNum = cursor.fetchone()[0]
                    if not initNum:
                        initNum = 0

                    Num = initNum + int(lis[3])

                    text = "update 顾客 set '%s'='%s' where 姓名='%s'" % (lis[2], Num, lis[0])

                    cursor.execute("update 顾客 set '%s'='%s' where 姓名='%s'" % (lis[2], Num, lis[0]))
                    conn.commit()

            elif lis[1] in phone:
                reply = QMessageBox.information(self, '提示', '对用户 %s\n充值:%s' % (lis[1], lis[2]), QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cursor.execute("select %s from 顾客 where 电话='%s' " % (lis[2], lis[1]))
                    initNum = cursor.fetchone()[0]
                    if not initNum:
                        initNum = 0
                    Num = initNum + int(lis[3])
                    cursor.execute("update 顾客 set '%s'='%s' where 电话='%s'" % (lis[2], Num, lis[1]))
                    conn.commit()
                    text = "update 顾客 set '%s'='%s' where 电话='%s'" % (lis[2], Num, lis[1])
            else:
                QMessageBox.information(self, '提示', '该用户不存在', QMessageBox.Yes)
        except sqlite3.ProgrammingError:
            QMessageBox.critical(self, "警告", "表未找到或SQL 语句存在语法错误\n请联系管理员\n错误代码:2345", QMessageBox.Yes)
            conn.rollback()
        except sqlite3.OperationalError:
            QMessageBox.critical(self, "警告", "数据库操作失败\n请联系管理员\n错误代码:2346", QMessageBox.Yes)
            conn.rollback()
        else:
            logging.info('【用户修改】%s' %text)
        finally:
            conn.close()

    def lookCust(self):
        self.lookCust_Data = DataGrid()
        self.lookCust_Data.show()

    def connect_LCD(self):
        try:
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            tempflag = False
            if self.cust_name.text().strip() != "":
                MONERY = "SELECT 药品可用金额,积分,电话 from 顾客 where 姓名 = '%s'" % (self.cust_name.text().strip())
                tempflag = True
            else:
                MONERY = "SELECT 药品可用金额,积分,姓名 from 顾客 where 电话='%s'" % (self.cust_phone.text().strip())
            cursor.execute(MONERY)
            print(MONERY)
            tempList = cursor.fetchone()
            print(tempList[0])
            self.money_vaild_2.display(tempList[0])
            self.jifen.display(tempList[1])
            if tempflag:
                self.label_5.setText("电话：" + str(tempList[2]))
            else:
                self.label_5.setText("姓名：" + str(tempList[2]))
            testList = cursor.fetchall()
            if testList:
                tempStr = ""
                for n in testList:
                    tempStr += n[2] + "\n"
                QMessageBox.warning(self, "提示", "与用户%s \n发生冲突" % tempStr)
            self.showThings2()  # 触发手法
            self.showThings()
        except TypeError:
            print(121212)
            self.money_vaild_2.display(0)
            self.jifen.display(0)
            self.showThings2()  # 触发手法
            self.showThings()
        finally:
            conn.close()

    def postError(self):
        #读取 邮箱 秘钥
        msg = MIMEText('hello,send by 医琦管理','plain','utf-8')
        to_addr = self.cfg.get('default','To_addr')
        from_addr = self.cfg.get('default','From_addr')
        password = self.cfg.get('default','Password')
        smtp_server = self.cfg.get('default','SMTP_server')
        server = smtplib.SMTP(smtp_server,25)
        server.set_debuglevel(1)
        server.login(from_addr,password)
        server.sendmail(from_addr,[to_addr],msg.as_string())
        server.quit()

    def add_Jifen(self):
        self.add_Jifen_temp = AddJifenData()
        self.add_Jifen_temp.show()
    # 关闭数据库
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.db.close()

    def Get_data(self):
        # 复选框、名称、价格、数量 [[],[],...]
        self.yaopin = [[self.showYaopin.cellWidget(i, 0),  self.showYaopin.item(i, 1),
                         self.showYaopin.item(i, 2), self.showYaopin.cellWidget(i, 5)]
                        for i in range(self.showYaopin.rowCount()) if
                        self.showYaopin.cellWidget(i, 0).checkState() == Qt.Checked
                        and self.showYaopin.cellWidget(i, 5).value() != 0]

        # 复选框、名称、剩余次数、使用次数
        self.shoufa = [[self.showShoufa.cellWidget(i, 0),  self.showShoufa.item(i, 1),
                         self.showShoufa.item(i, 4), self.showShoufa.cellWidget(i, 5)]
                        for i in range(self.showShoufa.rowCount()) if
                        self.showShoufa.cellWidget(i, 0).checkState() == Qt.Checked
                        and self.showShoufa.cellWidget(i, 5).value() != 0]
        return self.yaopin, self.shoufa

    def Check_money(self):
        try:
            sumThing = 0
            for tempList in self.yaopin:
                sumThing += float(tempList[2].text()) * float(tempList[3].value())

            if self.money_vaild_2.value() - sumThing < 0:
                QMessageBox.warning(self, "警告", "账号余额不足", QMessageBox.Yes)
            else:
                reply = QMessageBox.information(self, "提示", "商品消费 %s元" % sumThing, QMessageBox.Yes|QMessageBox.No)
                if reply == QMessageBox.Yes:
                    rest_money = self.money_vaild_2.value() - sumThing
                    return sumThing, rest_money
                else:
                    return None
        except Exception as e:
            QMessageBox.warning(self, "警告", "%s\n错误代码：999" % e)
            logging.warning(e)

    def Clearing_Yaopin(self):
        # 增加一个 数据结构
        # 如果正常 返回 积分、可用商品余额、商品名称和剩余次数的列表
        try:
            print("------结算药品-----")
            restThing = 0
            jifen = 0
            Thing_FinList = []
            keyongThing = 0
            sumThing = 0
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()

            for tempList in self.yaopin:
                if self.cust_name.text().strip():
                    cursor.execute("SELECT 库存数量 from things where 名称='%s'" % tempList[1].text())
                    for ThingOne in cursor.fetchall():
                        # 复选框、名称、价格、数量 [[],[],...]
                        if float(ThingOne[0]) - tempList[3].value() < 0:
                            print(QMessageBox.critical(self, '警告',
                                                       '%s商品库存不足\n现有库存%s' % (tempList[3].value(), self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                            raise Exception("商品库存不足")
                        else:
                            # 复选框、名称、价格、数量
                            restThing = float(ThingOne[0]) - float(tempList[3].value())
                            Thing_FinList.append([tempList[1].text(), restThing,tempList[2].text(),tempList[3].value()])

                elif self.cust_phone.text().strip():
                    cursor.execute("SELECT 库存数量 from things where 名称='%s'" % tempList[2])
                    for ThingOne in cursor.fetchall():
                        if float(ThingOne[0]) - tempList[3] < 0:
                            print(QMessageBox.critical(self, '警告',
                                                       '%s商品库存不足\n现有库存%s' % (tempList[2], self.query2.value(0)),
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                            raise Exception("商品库存不足")
                        else:
                            restThing = ThingOne[0] - tempList[3]
                            Thing_FinList.append([tempList[1].text(), restThing,tempList[2].text(),tempList[3].value()])
            sumThing, keyongThing = self.Check_money()
            jifen = float(self.jifen.value()) + float(sumThing)
        except IOError:
            return None
        except Exception as e:
            QMessageBox.warning(self, "警告", "%s\n错误代码：101" % e)
            logging.warning(e)
            return None
        else:
            return jifen, keyongThing, Thing_FinList, sumThing
        finally:
            conn.close()

    def Clearing_Shoufa(self):
        try:
            show_name= ""
            Hand_FinList = []
            # 复选框、名称、剩余次数、使用次数
            for Hand_num in self.shoufa:
                if int(Hand_num[2].text()) - int(Hand_num[3].value()) < 0:
                    raise Exception("%s 剩余次数不足" % Hand_num[1].text())
                else:
                    Rest_num = int(Hand_num[2].text()) - int(Hand_num[3].value())
                    Hand_FinList.append([Hand_num[1].text(), Rest_num,Hand_num[3].value()])  # 名称、数量
                    show_name += Hand_num[1].text()+str(Hand_num[3].value())+"次\n"
            reply = QMessageBox.information(self,"消费手法",show_name,QMessageBox.Yes,QMessageBox.No)
            if reply != QMessageBox.Yes:
                raise Exception("手法添加错误！")
        except Exception as e:
            QMessageBox.warning(self, "警告\n错误代码：74", "%s" % e, QMessageBox.Yes)
            logging.warning(e)
            return None
        else:
            return Hand_FinList

    def Flow(self):
        self.Get_data()
        now = datetime.datetime.today().strftime('%d/%m/%Y')
        try:
            conn = sqlite3.connect("data/all.db")
            if not self.lineEdit_2.text().strip():
                raise Exception("请输入工号")

            cursor = conn.cursor()
            logging.info("-----进入结算------")
            jifen, keyongThing, Thing_FinList,sumThing = self.Clearing_Yaopin()

            if self.cust_name.text().strip():
                cursor.execute("update 顾客 set 积分 = '%s',药品可用金额='%s' where 姓名 ='%s'" % (
                    jifen, keyongThing, self.cust_name.text().strip()))
                text1 = "【用户信息修改】%s 积分=%s,药品可用金额=%s" % (self.cust_name.text().strip(), jifen, keyongThing)
                logging.info(text1)
                # 更改商品信息
                for Thing in Thing_FinList:
                    cursor.execute("update things set 库存数量 = '%s' where 名称 ='%s'"
                                   % (Thing[1], Thing[0]))
                    print("update things set 库存数量 = '%s' where 名称 ='%s'"
                                   % (Thing[1], Thing[0]))
                    text2 = "【商品信息修改】%s 库存数量=%s " % (Thing[1],Thing[0])
                    print(text2)
                    logging.info(text2)
            elif self.cust_phone.text().strip():
                cursor.execute("update 顾客 set 积分 = '%s',药品可用金额='%s' where 电话 ='%s'"
                               % (jifen, keyongThing, self.cust_phone.text().strip()))
                text = "【用户信息修改】%s 积分=%s,药品可用金额=%s" % (self.cust_phone.text().strip(), jifen, keyongThing)
                logging.info(text)
                # 更改商品信息
                for Thing in Thing_FinList:
                    cursor.execute("update things set 库存数量 = '%s' where 名称 ='%s'"
                                   % (Thing[1], Thing[0]))
                    text2 = "【商品信息修改】%s 库存数量=%s " % (Thing[0], Thing[1])
                    logging.info(text2)

            Hand_FinList = self.Clearing_Shoufa()
            if self.cust_name.text().strip():
                for temp in Hand_FinList:
                   # print("update 顾客 set '%s' = '%s' where 姓名 ='%s'" % (str(temp[0]), temp[1], self.cust_name.text()))
                    cursor.execute(
                        "update 顾客 set '%s' = '%s' where 姓名 ='%s'" % (str(temp[0]), temp[1], self.cust_name.text()))
                    text3 = "【修改用户信息】顾客 %s set %s='%s'" % (self.cust_name.text(), temp[0], temp[1])
                    logging.info(text3)
            elif self.cust_phone.text().strip():
                for temp in Hand_FinList:
                    cursor.execute("update 顾客 set '%s' = '%s' where 电话 ='%s'" % (
                        str(temp[0]), temp[1], self.cust_phone.text()))
                    text3 = "【修改用户信息】电话:%s %s=%s" % (self.cust_phone.text(), temp[0], temp[1])
                    logging.info(text3)

            logtemp = Hand_FinList + Thing_FinList
            # 提交到log数据表
            if self.cust_name.text().strip():
                cursor.execute(
                    'insert into log(顾客姓名,购买记录,购买时间,工号,金额) values("%s","%s","%s","%s","%s")'
                    % (self.cust_name.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sumThing))
            elif self.cust_phone.text().strip():
                cursor.execute('insert into log(电话,购买记录,购买时间,工号,金额)values("%s","%s","%s","%s","%s")'
                               % (self.cust_phone.text().strip(), logtemp, now, self.lineEdit_2.text().strip(), sumThing))

            publish_previous_list = [self.cust_name.text().strip(),self.cust_phone.text().strip(),Thing_FinList,sumThing,keyongThing,Hand_FinList]

            with open("ppx.json","w",encoding="utf-8") as fd:
                fd.write(json.dumps(publish_previous_list))

            Printmain(name = self.cust_name.text().strip(), phone = self.cust_phone.text().strip(), data=Thing_FinList, fin=sumThing, keyongThing=keyongThing,Hand_FinList=Hand_FinList)  # 打印小票信息
            reply = QMessageBox.information(self,"提示","是否继续打印小票？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                Printmain(name=self.cust_name.text().strip(), phone=self.cust_phone.text().strip(), data=Thing_FinList,
                          fin=sumThing, keyongThing=keyongThing, Hand_FinList=Hand_FinList)  # 打印小票信息
            else:pass
        except TypeError:
            QMessageBox.critical(self, "警告", "重新选择项目", QMessageBox.Yes)
            conn.rollback()
            logging.info("-----以上消息失效------")
        except IOError:
            QMessageBox.critical(self, "警告", "检查数据库连接\n并与管理员联系\n错误代码:3456", QMessageBox.Yes)
            conn.rollback()
            logging.info("-----以上消息失效------")
        except sqlite3.OperationalError:
            QMessageBox.critical(self, "警告", "数据库操作失败\n并与管理员联系\n错误代码:3457", QMessageBox.Yes)
            conn.rollback()
            logging.info("-----以上消息失效------")
        except UnboundLocalError:
            QMessageBox.critical(self, "警告", "检查打印机连接\n或与管理员联系\n错误代码:3458", QMessageBox.Yes)
            conn.rollback()
            logging.info("-----以上消息失效------")

        except Exception as e:
            QMessageBox.critical(self, "警告\n错误代码：78", "%s" % e, QMessageBox.Yes)
            conn.rollback()
            logging.error(e)
            logging.info("-----以上消息失效------")
        else:
            conn.commit()
        finally:
            conn.close()
            # 初始化
            self.cust_name.setText("")
            self.cust_phone.setText("")
            self.label_5.setText(" ")
            self.showShoufa.clear()
            self.showYaopin.clear()

class update_Thread(QThread,Ui_mainWindow):
    update_Signal = pyqtSignal(bool)
    def __init__(self):
        super(update_Thread,self).__init__()

    def run(self):
        # 确定当前软件是否为最新版
        try:
            params = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
                "Host": "api.github.com"}
            response = requests.get("https://api.github.com/repos/zhihao2020/ShopSystem/releases/latest", params=params)
            while response.status_code != 200:
                time.sleep(1200)

            temp = json.loads(response.text)
            self.latest_tag = temp["tag_name"]
            print(self.latest_tag)
            if not os.path.exists("softID.io"):
                file = open("softID.io","w")
                file.close()
            with open("softID.io",'r') as f:
                previous_tag = f.readline()
            if self.latest_tag != previous_tag:
                with open("update.ini","w") as f_update:
                    download_url = temp["assets"][0]['browser_download_url']
                    file_size = temp['assets'][0]['size']
                    f_update.write("%s,%s,%s"%(download_url, file_size,1))
                    self.update_Signal.emit(True)
        except requests.exceptions.ConnectionError:
            time.sleep(1200)
            self.check_latest()

class Thread(QThread,Ui_mainWindow):
    #检测用户无输入，自动休眠
    sleep_signal = pyqtSignal(bool)
    information_signal = pyqtSignal(bool)
    def __init__(self):
        super(Thread, self).__init__()
        self.config = ConfigParser()
        self.config.read("config.ini")

    def run(self):
        while True:
            num = 0
            previousPostion = pyautogui.position()
            print(previousPostion)
            self.information_signal.emit(False)
            time.sleep(1)
            while previousPostion == pyautogui.position():
                num +=1
                time.sleep(1)
                if num > self.config.getint('default','sleep_time')-5:
                    self.information_signal.emit(True)
                    if num >  self.config.getint('default','sleep_time'):
                        self.sleep_signal.emit(True)

class Information(QWidget):
    def __init__(self):
        super(Information,self).__init__()
        self.initUI()
    def initUI(self):
        label = QLabel(self)
        label.resize(700, 100)
        label.setText("还有5秒钟，关闭软件")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QtGui.QFont("Arial", 40))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = reload_mainWin()
    myWin.show()
    sys.exit(app.exec_())
