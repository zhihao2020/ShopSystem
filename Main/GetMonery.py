def jiesuan(self, name):
    lines = []
    sum = 0
    i = 0
    if (i < self.name.rowCount()):
        ###################                    #√，名称，单价，数量
        lines.append([self.tableWidget.cellWidget(i, 0), self.tableWidget.item(i, 1), self.tableWidget.item(i, 2),
                      self.tableWidget.cellWidget(i, 5)])
        i += 1
    for line in lines:
        if line[0].isChecked():
            self.di[line[1].text()] = float(line[3].value)  # 加入已选的名称
            sum += float(line[2].text()) * float(line[3].value())

    print(sum)
    print("最后价格：", sum * float(self.lineEdit_4.text()))
    fin = sum * float(self.lineEdit_4.text())

    pan = 0

    if self.cust_name.text():
        pan = 1
    elif self.cust_phone.text():
        pan = 2
    else:
        pan = 3
        print(QMessageBox.information(self, '提示', '结算 进入 散客模式', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No))
    reply = QMessageBox.information(self, '提示', '消费金额%s' % fin, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    if reply == QMessageBox.Yes:

        if pan == 1:
            self.query.exec_("SELECT 积分,可用金额,累计金额 from 商品 where 姓名 = '%s'" % self.cust_name.text())
            # 更改商品信息
            for name in self.Di.keys():
                print("结算", name)
                self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                while (self.query2.next()):
                    if (float(self.query2.value(0)) - self.Di[name] < 0):
                        print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                    else:
                        self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                          % (float(self.query2.value(0)) - self.Di[name], name))
            # 更改用户信息
            while (self.query.next()):
                jifen = self.query.value(0)
                keyong = self.query.value(1)
                leiji = self.query.value(2)

            self.query.exec_("update 顾客 set 积分 = '%s',可用金额='%s',累计金额='%s' where 姓名 ='%s'"
                             % (jifen, keyong, leiji, self.cust_name.text()))

        elif pan == 2:
            self.query.exec_("SELECT 积分,可用金额,累计金额 from 商品 where 电话 = '%s'" % self.cust_phone.text())

            for name in self.Di.keys():
                print("结算", name)
                self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                while (self.query2.next()):
                    if (float(self.query2.value(0)) - self.Di[name] < 0):
                        print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                    else:
                        self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                          % (float(self.query2.value(0)) - self.Di[name], name))

            while (self.query.next()):
                jifen = self.query.value(0)
                keyong = self.query.value(1)
                leiji = self.query.value(2)

            self.query.exec_("update 顾客 set 积分 = '%s',可用金额='%s',累计金额='%s' where 电话 ='%s'" % (
                jifen, keyong, leiji, self.cust_phone.text()))
            self.query.exec_()

        else:
            for name in self.Di.keys():
                print("结算", name)
                self.query2.exec_("SELECT 数量 from 商品 where 名称='%s'" % name)
                while (self.query2.next()):
                    if (float(self.query2.value(0)) - self.Di[name] < 0):
                        print(QMessageBox.critical(self, '警告', '%s商品库存不足\n先有库存%s' % (name, self.query2.value(0)),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No))
                    else:
                        self.query2.exec_("update 商品 set 数量 = '%s' where 名称 ='%s'"
                                          % (float(self.query2.value(0)) - self.Di[name], name))
