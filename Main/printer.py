# coding=utf-8
import win32print
import logging
import textwrap
from PyQt5.QtWidgets import QMessageBox
class Printer:
    def __init__(self):
        #使用的打印机 名称
        self.PRINTER_NAME = "Blu-ray-58"
        self.LINE_WIDTH = 40
        self.lines = []
    def wrap(self, data, width=None):
        if data == "":
            return " "

        if width is None:
            width = self.LINE_WIDTH

        split = [data[i] for i in range(0, len(data))]
        orig_str = "".join(split)
        new_str = "\n".join(textwrap.wrap(orig_str, width))
        return new_str

    def add_line(self, data):
        self.lines.append(self.wrap(data))

    def output(self):
        try:
            hPrinter = win32print.OpenPrinter(self.PRINTER_NAME)
        except:

            logging.error("没有连接打印机 或 没有配置打印机")
        try:
            win32print.StartDocPrinter(hPrinter, 1, ("Notification", None, "RAW"))
            try:
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, "\n".join(self.lines).encode("GBK"))
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

            self.lines = []
