#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets
from data import *
from calendar import *

class QueryWindow(QWidget):

    def __init__(self, user):
        super(QueryWindow, self).__init__()
        self.user = user
        self.setWindowTitle("查询")
        self.setFixedSize(800, 600)
        self.set_ui()

    def set_ui(self):
        self.db = DataBase()
        self.db.cur.execute("select hospital_id from user where username = '%s'"%(self.user))
        hospital_id = self.db.cur.fetchone()[0]
        self.db.cur.execute("select * from death_info where hospital_code = '%s'"%(hospital_id))
        rslt = self.db.cur.fetchall()
        amount = len(rslt)
        self.db.cur.execute("select name from hospital")
        hospital = self.db.cur.fetchall()
        hospital_list = [i[0] for i in hospital]
        self.name_label = QLabel("姓名")
        self.name = QLineEdit()
        self.begin_date_label = QLabel("起始日期")
        self.begin_date = QDateEdit()
        self.begin_date_bnt = QPushButton()
        self.begin_date_bnt.setStyleSheet("border:hidden;")
        self.begin_date_bnt.setIcon(QIcon('cal2.png'))
        self.begin_date_bnt.clicked.connect(self.begin_date_choose)
        self.end_date_label = QLabel("截止日期")
        self.end_date = QDateEdit()
        self.end_date_bnt = QPushButton()
        self.end_date_bnt.setStyleSheet("border:hidden;")
        self.end_date_bnt.setIcon(QIcon('cal2.png'))
        self.end_date_bnt.clicked.connect(self.end_date_choose)
        self.department_label = QLabel("单位")
        self.department = QComboBox()
        for i in hospital_list:
            self.department.addItem(i)
            
        self.table = QTableWidget(amount,12)


        self.head_layout = QHBoxLayout()
        self.head_layout.addWidget(self.name_label)
        self.head_layout.addWidget(self.name)
        self.head_layout.addWidget(self.begin_date_label)
        self.head_layout.addWidget(self.begin_date)
        self.head_layout.addWidget(self.begin_date_bnt)

        self.setLayout(self.head_layout)

    def begin_date_choose(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_begin_date)

    def input_begin_date(self, date):
        self.begin_date.setDate(date)

    def end_date_choose(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_end_date)

    def input_end_date(self, date):
        self.end_date.setDate(date)
