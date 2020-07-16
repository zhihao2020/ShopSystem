from PyQt5.QtWidgets import QWidget,QMessageBox
from UI.add.addJifen import Ui_Form
import sqlite3

class AddJifenData(QWidget,Ui_Form):
    def __init__(self):
        super(AddJifenData, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.push)

    def add(self):
        self.name = []
        self.phone = []
        conn = sqlite3.connect("data/all.db")
        cursor = conn.cursor()
        temp = cursor.execute("SELECT 姓名,电话 FROM 顾客")
        for n in temp.fetchall():
            self.name.append(n[0])
            self.phone.append(n[1])
        conn.close()
    def push(self):
        self.add()
        try:
            conn = sqlite3.connect("data/all.db")
            cursor = conn.cursor()
            if self.lineEdit.text().strip() in self.name:
                cursor.execute("SELECT 积分 FROM 顾客 WHERE 姓名='%s'"%self.lineEdit.text().strip())
                num = cursor.fetchone()[0]
                print(num)
                finNum = float(num) + float(self.spinBox.value())
                cursor.execute("update 顾客 set 积分 = '%s' where 姓名 ='%s'"%(finNum,self.lineEdit.text().strip()) )
                self.spinBox_2.value=0
                self.add_thing_name.setText("")
                self.lineEdit.setText("")
                conn.commit()
            elif self.lineEdit_2.text().strip() in self.phone:
                cursor.execute("SELECT 积分 FROM 顾客 WHERE 电话='%s'" % self.lineEdit_2.text().strip())
                num = cursor.fetchone()[0]
                finNum = float(num) + float(self.spinBox.value())
                cursor.execute("update 顾客 set 积分 = '%s' where 电话 ='%s'" % (finNum, self.lineEdit_2.text().strip()))
                self.spinBox_2.value = 0
                self.add_thing_name.setText("")
                self.lineEdit.setText("")
                conn.commit()
            else:
                print(QMessageBox.information(self,"提示","用户不存在",QMessageBox.Yes))
        except:
            print(QMessageBox.critical(self, "警告", "充值失败\n错误代码:7879\n请联系管理人员", QMessageBox.Yes))
        else:
            print(QMessageBox.information(self,"提示","充值成功\n充值:%s"%finNum,QMessageBox.Yes))
        finally:
            conn.close()