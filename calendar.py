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

class Calendar_With_Clock(QWidget):

    datetime_signal = pyqtSignal(QDateTime)

    def __init__(self):
        super(Calendar_With_Clock,self).__init__()
        self.setWindowTitle('日历')
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.hour = QComboBox()
        for i in range(24):
            self.hour.addItem(str(i))
        self.minute = QComboBox()
        for j in range(60):
            self.minute.addItem(str(j))
        self.bnt = QPushButton("确定")
        self.bnt.clicked.connect(self.show_datetime)

        self.clock = QHBoxLayout()
        self.clock.addWidget(self.hour)
        self.clock.addWidget(QLabel("时"))
        self.clock.addWidget(self.minute)
        self.clock.addWidget(QLabel("分"))
        self.clock.addWidget(self.bnt)
        self.clock_layout = QWidget()
        self.clock_layout.setLayout(self.clock)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.cal)
        self.vbox.addWidget(self.clock_layout)
        # self.vbox.addWidget(self.bnt)

        self.setLayout(self.vbox)

    def show_datetime(self):
        date = self.cal.selectedDate()
        datetime = QDateTime.currentDateTime()
        datetime.setDate(date)
        datetime.setTime(QTime(int(self.hour.currentText()), int(self.minute.currentText())))
        self.datetime_signal.emit(datetime)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Calendar_With_Clock()
    mainwindow.show()
    sys.exit(app.exec_())
