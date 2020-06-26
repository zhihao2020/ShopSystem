from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from UI.lookCust import Ui_Form
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

class lookCustData(QWidget,Ui_Form):
    def __init__(self):
        super(lookCustData, self).__init__()
        self.setupUi(self)
        self.db = QSqlDatabase.addDatabase('QSQLITE', "db3")
        self.db.setDatabaseName('../data/all.db')
        self.db.open()
        self.query = QSqlQuery(self.db)
        self.lineEdit.textChanged.connect(self.showInfo)
        self.lineEdit_3.textChanged.connect(self.showInfo)
        self.lineEdit_4.textChanged.connect(self.find_Thing)

    def get_Row(self):
        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes))
        try:
            n = 0
            if self.lineEdit.text():
                self.query.exec_("SELECT * from log where 顾客姓名='{}'".format(self.lineEdit.text()))
                print("SELECT * from log where 顾客姓名='{}'".format(self.lineEdit.text()))
            elif self.lineEdit_3.text():
                self.query.exec_("SELECT * from log where 电话='{}'".format(self.lineEdit_3.text()))
            while (self.query.next()):
                n += 1
            print("数据库中有", n, "行")
            return n
        except:
            print(QMessageBox.critical(self, "警告", "输入顾客 姓名或电话", QMessageBox.Yes))
            pass
    def click(self,item):
        QMessageBox.information(self,"信息",self.tableWidget.item(item.row(),0).text())

    def showInfo(self):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(self.get_Row())
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["购买记录","购买时间","金额","工号"])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格自适应
        self.tableWidget.clicked.connect(self.click)
        i = 0
        if self.lineEdit.text():
            self.query.exec_("SELECT 购买记录,购买时间,金额,工号 from log where 顾客姓名='%s'" % self.lineEdit.text())

        elif self.lineEdit_3.text:
            self.query.exec_("SELECT 购买记录,购买时间,金额,工号 from log where 电话='%s'" % self.lineEdit_3.text())

        while (self.query.next()):
            for n in range(4):
                newItem = QTableWidgetItem(str(self.query.value(n)))
                self.tableWidget.setItem(i,n, newItem)
            i += 1
        self.tableWidget.show()

    def find_Thing(self):
        try:
            items = self.tableWidget.findItems(self.lineEdit_4.text(), QtCore.Qt.MatchStartsWith)
            if len(items) > 0:
                for n in range(items):
                    print(n)
                    item = items[n]
                    item.setSelected(True)
                item = items[0]
                row = item.row()
                # 定位到指定的行
                self.tableWidget.verticalScrollBar().setSliderPosition(row)
        except:
            pass

    def getData(self):
        money = []
        log = []
        logTime = []
        if self.lineEdit_3.text():
            self.query.exec_("select 购买记录,购买时间,金额 from log where 电话='%s'"%(self.lineEdit_3.text()))
        elif self.lineEdit.text():
            self.query.exec_("select 购买记录,购买时间,金额 from log where 姓名='%s'"%(self.lineEdit.text()))
        num = 0
        while(self.query.next()):
            log.append(self.query.value(0))
            logTime.append(self.query.value(1))
            money.append(self.query.value(2))

            for x in log:
                for y in x:
                    if y[0] == self.lineEdit_5.text():
                        num +=1
        self.showPicture(log,logTime,money)

    def showPicture(self,log,logTime,money):

        plt.rcParams['font.sans-serif'] = ['SimHei']

        # 设置时间戳作为横轴刻度
        xs = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in logTime]
        ys = money
        # 设置绘图框的大小
        fig = plt.figure(figsize=(10, 6))

        # 添加标题和坐标轴标签
        plt.title('顾客消费情况图')
        plt.xlabel('购买日期')
        plt.ylabel('消费金额')

        # 获取图的坐标信息
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        # 设置图例显示
        plt.legend(bbox_to_anchor=[1, 1])

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且60度倾斜
        fig.autofmt_xdate(rotation=60)
        plt.plot(xs,ys)
        # 显示图形
        plt.show()

    def closeEvent(self, event):
        pass



