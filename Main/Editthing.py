from UI.EditThings import Ui_Form
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtWidgets import *

class editThing(QWidget,Ui_Form):
    def __init__(self):
        super(editThing, self).__init__()
        self.setupUi(self)

        self.db = QSqlDatabase.addDatabase('QSQLITE', "db3")
        self.db.setDatabaseName(r"data\all.db")
        self.db.open()

        if self.db.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes, QMessageBox.Yes))
        else:
            print("OK")
        self.querys_11 = QSqlQuery(self.db)
        self.querys_22 = QSqlQuery(self.db)
        self.modify = True

        self.show_thing()

        self.pushButton.clicked.connect(self.edit_vaild)
        self.pushButton_2.clicked.connect(self.del_thing)
        self.pushButton_3.clicked.connect(self.find_thing)

    #让表格可以修改，并保存到数据库中
    def edit_vaild(self):
        print(QMessageBox.critical(self, "警告", "数据将可以修改", QMessageBox.Yes, QMessageBox.Yes))
        self.modify = False
        self.show_thing()

    def del_thing(self):
        pass

    def find_thing(self):
        pass

    def get_sql_row_num(self):
        ro=0
        self.querys.exec_("SELECT 名称 from 商品 ")
        while(self.querys.next()):
            ro +=1
        return ro

    def show_thing(self):
        row = 0

        self.tableWidget.setRowCount(self.get_sql_row_num())
        self.tableWidget.setColumnCount(3)

        if self.modify:
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可修改
        else: self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked) #双击表格可以修改

        # 设置TableWidget的标签
        self.tableWidget.setHorizontalHeaderLabels(['名称', '单价', '备注'])

        # 让表格充满整个窗口
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 通过遍历 让表格充满数据
        self.querys_11.exec_("SELECT 名称 from 商品 ")
        while (self.querys.next()):
            self.querys_22.exec_("SELECT * from 商品 where 名称 = '%s'" % self.querys_11.value(0))
           # print("SELECT 名称,单价,备注 from 商品 where 名称='%s'" % self.querys_22.value(0))
            while (self.querys_22.next()):
                column = 0
                for n in range(3):
                    print("two:", self.querys_22.value(n))
                    newItem = QTableWidgetItem(str(self.querys_22.value(n)))
                    self.tableWidget.setItem(row, column, newItem)
                    print(row, column)
                    column += 1
            row += 1