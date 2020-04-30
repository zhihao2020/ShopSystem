from PyQt5.QtGui import QFont,QTextDocument,QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy, QAction,QDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog
import datetime
import pdfkit

def makeHtml(log):
    GEN_HTML = "../images/demo_1.html"

    now = datetime.datetime.today().strftime('%d/%m/%Y')
    shouyinYuan = "001"
    thingS="""
    <tr>
                            <td>今麦郎</td>
                            <td>1</td>
                            <td>100.00</td>
                        </tr>
    """


    f = open(GEN_HTML,'w',encoding='utf-8')
    message = """"<!DOCTYPE html>   
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>使用PyQt5打印热敏小票</title>
    </head>
    <style type="text/css">
        * {padding:0;margin: 0;}
        h1 {font-size: 20px;}
        h3 {font-size: 16px;}
        .left {float: left;}
        .right {float:right;}
        .clearfix {clear: both;}
        ul {list-style: none;}
        .print_container {width: 250px;}
        .section2 label {display: block;}
        .section3 label {display: block;}
        .section4 .total label {display: block;}
        .section4 {border-bottom: 1px solid #DADADA;}
        .section5 label {display: block;}
    </style>
    <body>
    <div id="capture">
        <div class="print_container">
            <h3>医琦健康</h3>
            <span>***************************************</span>
            <div class="section3">
                <label>下单时间：%s</label>
                <label>收银员:%s</label>
            </div>
            <span>***************************************</span>
            <div class="section4">
                <div style="border-bottom: 1px solid #DADADA;">
                    <table style="width: 100%%;">
                        <thead>
                        <tr>
                            <td width="60%%">品名</td>
                            <td width="20%%">数量</td>
                            <td width="20%%">金额</td>
                        </tr>
                        </thead>
                        <tbody>
                        %s
                        </tbody>
                    </table>
                </div>
                <div class="total">
                    <label class="left">合 计</label>
                    <label class="right">%s</label>
                    <div class="clearfix"></div>
                    <label class="left">收款金额</label>
                    <label class="right">%s</label>
                    <div class="clearfix"></div>
                    <label class="left">找零金额</label>
                    <label class="right">%s</label>
                    <div class="clearfix"></div>
                </div>
                <span>***************************************</span>
            </div>
            <div class="section5">
                <label>欢迎光临，谢谢惠顾！</label>
                <label>医琦健康中心</label>
            </div>
        </div>
    </div>
    </body>
    </html>
    """%(now,shouyinYuan,thingS,100,100,100) #下单时间，收银员，商品,#合计，收款，找零
    f.write(message)
    f.close()

def HtmltoPic():
    pdfkit.from_file('../images/demo.html', '../images/out.pdf')


def on_printAction1_triggered(self):

    printer = QPrinter()
    printDialog = QPrintDialog(printer, self)
    if printDialog.exec_() == QDialog.Accepted:
        handlePaintRequest(printer)

def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        cursor.insertText(self.label.text())
        document.print(printer)