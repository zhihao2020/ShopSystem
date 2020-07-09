from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from UI.InTo import Ui_widget
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtCore import  pyqtSignal
import myMainWindow
import sys

class Load_login(QMainWindow,Ui_widget):
    is_admin_signal = pyqtSignal()
    def __init__(self):
        super(Load_login,self).__init__()
        self.setupUi(self)
        self.InTo.clicked.connect(self.post_to_sql)
        self.is_admin_signal.connect(self.jump)


    def post_to_sql(self):
        dbs = QSqlDatabase.addDatabase('QSQLITE')
        dbs.setDatabaseName(r'data/password.db')
        if dbs.open() is None:
            print(QMessageBox.critical(self, "警告", "数据库连接失败，请查看数据库配置", QMessageBox.Yes, QMessageBox.Yes))
        querys = QSqlQuery()
        sql = "SELECT * FROM  password where ID = '%s'" % self.name.text()
        querys.exec_(sql)

        if(not querys.next()):
            print(QMessageBox.information(self,"提示","该账号不存在",QMessageBox.Yes,QMessageBox.Yes))
        else:
            if (self.name.text() == querys.value(0) and self.Password.text() == querys.value(1)):
                dbs.close()
                self.is_admin_signal.emit()
            else:
                print(QMessageBox.information(self, "提示", "密码错误", QMessageBox.Yes, QMessageBox.Yes))

    def jump(self):
        print("hello")
        self.close()
        self.jumper = myMainWindow.reload_mainWin()
        self.jumper.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    myWin = Load_login()
    myWin.show()
    sys.exit(app.exec_())