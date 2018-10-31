#!/usr/bin/env python
#coding:utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from data import *

class Import_Window(QWidget):

    def __init__(self):
        super(Import_Window,self).__init__()
        self.setWindowTitle("导入数据")
        self.setFixedSize(400,300)
        self.set_ui()

    def set_ui(self):

        self.filename = QLineEdit()
        self.bnt = QPushButton("导入CSV文件")
        self.bnt.clicked.connect(self.import_data)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.bnt)
        self.setLayout(self.layout)

    def import_data(self):
        self.db = DataBase()
        filename,ok = QFileDialog.getOpenFileName(self, '打开文件','./')
        self.filename.setText(filename)
        with open(filename,'r') as f:
            pass
