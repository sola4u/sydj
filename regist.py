#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys
from address import *
from calendar import *

class Regist(QWidget):

    def __init__(self):
        super(Regist,self).__init__()
        self.setWindowTitle("登记")
        self.resize(420, 600)
        self.set_ui()

    def set_ui(self):

        self.layout = QVBoxLayout()

        self.back_bnt = QPushButton('返回(ESC)')
        self.back_bnt.clicked.connect(self.back_click)

        self.print_bnt = QPushButton('打印(F5)')
        self.print_bnt.clicked.connect(self.print_record)

        self.save_bnt = QPushButton('保存(F2)')
        self.save_bnt.clicked.connect(self.save_record)

        self.add_bnt = QPushButton('添加(F1)')
        self.add_bnt.clicked.connect(self.add_record)

        self.number_label = QLabel('编号')
        self.number = QLineEdit()
        self.number2 = str(QDateTime.currentDateTime().toPyDateTime()).replace('/',
                            '').replace(' ','').replace(':','').replace('.','').replace('-','')[:-3]
        self.number.setPlaceholderText(self.number2)
        self.number.setReadOnly(True)

        self.namelabel = QLabel('姓名')
        self.name = QLineEdit()

        self.genderlabel = QLabel('性别')
        self.gender = QLineEdit()
        self.male = QCheckBox('男')
        self.male.stateChanged.connect(self.gender_male)
        self.female = QCheckBox('女')
        self.female.stateChanged.connect(self.gender_female)

        self.racelabel = QLabel('民族')
        self.race = QComboBox()
        self.race.setEditable(True)
        self.race.addItem('汉族')
        self.race.addItem('回族')
        self.race.addItem('壮族')
        self.race.addItem('藏族')
        self.race.addItem('维吾尔族')

        self.idlabel = QLabel('证件号码')
        self.id = QLineEdit()
        self.id_bnt = QLabel('请按回车ENTER')
        self.id.returnPressed.connect(self.id_to_date)

        self.birthlable = QLabel('出生日期')
        self.birthday = QDateEdit()
        self.birthchoice = QPushButton('>')
        self.birthchoice.clicked.connect(self.show_birth_cal)


        a = Address()
        a.location_label.setText("address_now")
        a.id_label.setText("code_now")
        self.address_now = a.location
        self.code_now = a.id
        b = Address()
        b.location_label.setText("address_birth")
        b.id_label.setText("code_birth")
        self.address_birth= b.location
        self.code_birth= b.id

        self.deathlabel = QLabel('死亡日期')
        self.deathdate = QDateEdit()
        self.deathchoice = QPushButton('>')
        self.deathchoice.clicked.connect(self.show_death_cal)

        self.diseaselabel = QLabel('死因')
        self.disease = QLineEdit()

        self.regist_date_lable = QLabel('登记日期')
        self.regist_date = QDateEdit(QDate.currentDate())
        self.regist_date_choice = QPushButton('>')
        self.regist_date_choice.clicked.connect(self.show_regist_cal)

        self.familylabel = QLabel('家属姓名')
        self.family = QLineEdit()

        self.tellabel= QLabel('联系方式')
        self.tel = QLineEdit()

        self.layout.addWidget(a)
        self.layout.addWidget(b)
        self.layout.addWidget(self.save_bnt)
        self.setLayout(self.layout)


    def back_click(self):
        pass

    def save_record(self):
        pass

    def print_record(self):
        pass

    def add_record(self):
        pass

    def gender_male(self, state):
        if state == Qt.Checked:
            self.gender.setText("男性")
            self.female.setChecked(False)

    def gender_female(self, state):
        if state == Qt.Checked:
            self.gender.setText("女性")
            self.male.setChecked(False)

    def id_to_date(self):
        id_upper = self.id.text().upper()
        if len(id_upper) == 18:
            self.id.setText(id_upper)
            year = int(id_upper[6:10])
            month =int(id_upper[10:12])
            day = int(id_upper[12:14])
            self.birthday.setDate(QDate(year,month,day))
            gender = int(id_upper[-2])
            if gender%2==0:
                self.female.setChecked(True)
                self.male.setChecked(False)
            else:
                self.female.setChecked(False)
                self.male.setChecked(True)

            certify_number = ['1','0','X','9','8','7','6','5','4','3','2','1']
            std_number = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
            sum = 0
            for i in range(17):
                sum += int(id_upper[i])*std_number[i]
            certify_rslt = certify_number[sum%11]
            if certify_rslt != id_upper[-1]:
                self.id_bnt.setText('身份证号码不正确')
                self.id_bnt.setStyleSheet('QLabel{color:red}')
            else:
                self.id_bnt.setText('请按回车ENTER')
        else:
            self.id_bnt.setText('请按回车ENTER')

    def show_birth_cal(self):
        cal = Calendar()
        cal.show()
        cal.date_signal.connect(self.input_birthday)

    def input_birthday(self, date):
        self.birthday.setDate(date)

    def show_death_cal(self):
        cal = Calendar()
        cal.show()
        cal.date_signal.connect(self.input_deathday)

    def input_deathday(self, date):
        self.deathdate.setDate(date)

    def show_regist_cal(self):
        cal = Calendar()
        cal.show()
        cal.date_signal.connect(self.input_registday)

    def input_registday(self, date):
        self.regist_date.setDate(date)






if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Regist()
        mainwindow.show()
        sys.exit(app.exec_())
