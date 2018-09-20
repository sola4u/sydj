#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import address_dic
import sys

class Address(QWidget):

    def __init__(self):
        super(Address,self).__init__()
        self.setFixedSize(500,200)
        self.province_list = address_dic.province_dic
        self.city_list = address_dic.city_dic
        self.county_list = address_dic.county_dic
        self.town_list = address_dic.town_dic
        self.set_ui()

    def set_ui(self):
        self.province_label = QLabel("省")
        self.province = QComboBox()
        self.city_label = QLabel("市")
        self.city = QComboBox()
        self.county_label = QLabel("县")
        self.county = QComboBox()
        self.town_label = QLabel("乡")
        self.town = QComboBox()
        self.id_label = QLabel('id')
        self.id = QLineEdit()
        self.location_label = QLabel("address")
        self.location = QLineEdit()
        self.province.currentTextChanged.connect(self.choose_city)
        self.city.currentTextChanged.connect(self.choose_county)
        self.county.currentTextChanged.connect(self.choose_town)
        self.town.currentTextChanged.connect(self.show_code)


        for i, j in self.province_list.items():
            self.province.addItem(j,QVariant(i))

        self.layout = QGridLayout()
        # self.layout.setRowStretch(0,1)
        # self.layout.setRowStretch(1,2)
        # self.layout.setRowStretch(2,1)
        # self.layout.setRowStretch(3,2)

        self.toplayout = QVBoxLayout()
        self.layout.addWidget(self.province_label,0,0)
        self.layout.addWidget(self.province,0,1,1,2)
        self.layout.addWidget(self.city_label,0,3)
        self.layout.addWidget(self.city,0,4,1,2)
        self.layout.addWidget(self.county_label,1,0)
        self.layout.addWidget(self.county,1,1,1,2)
        self.layout.addWidget(self.town_label,1,3)
        self.layout.addWidget(self.town,1,4,1,2)
        self.layout.addWidget(self.location_label,2,0)
        self.layout.addWidget(self.location,2,1,1,5)
        self.layout.addWidget(self.id_label,3,0)
        self.layout.addWidget(self.id,3,1,1,5)

        self.a = QWidget()
        self.a.setLayout(self.layout)
        self.toplayout.addWidget(self.a)

        self.setLayout(self.toplayout)

    def choose_city(self):
        province_id = self.province.currentData()
        self.city.clear()
        self.county.clear()
        self.town.clear()
        for i, j in self.city_list[province_id].items():
            self.city.addItem(j, QVariant(i))

    def choose_county(self):
        city_id = self.city.currentData()
        self.county.clear()
        if city_id:
            for i, j in self.county_list[city_id].items():
                self.county.addItem(j, QVariant(i))

    def choose_town(self):
        self.town.clear()
        county_id = self.county.currentData()
        if county_id:
            for i, j in self.town_list[county_id].items():
                self.town.addItem(j, QVariant(i))

    def show_code(self):
        self.id.setText(self.town.currentData())
        address_detail = self.province.currentText() + self.city.currentText() + self.county.currentText() + self.town.currentText()
        self.location.setText(address_detail)


if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Address()
        mainwindow.show()
        sys.exit(app.exec_())
