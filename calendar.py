#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import  *
import sys



class Calendar(QWidget):

    date_signal = pyqtSignal(QDate)

    def __init__(self):
        super(Calendar, self).__init__()
        self.setWindowTitle("日历")
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked.connect(self.show_date)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.cal)
        self.setLayout(self.vbox)

    def show_date(self):
        date = self.cal.selectedDate()
        self.date_signal.emit(date)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Calendar()
    mainwindow.show()
    sys.exit(app.exec_())
