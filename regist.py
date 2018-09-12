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

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(2,1)
        self.layout.setColumnStretch(3,1)

        self.report_distinct_lable = QLabel("报告地区")
        self.report_distinct = QLineEdit()
        self.report_distinct.setReadOnly(True)

        self.report_depart_lable = QLabel("报告单位")
        self.report_department = QLineEdit()

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
        self.unkonwn_gender = QCheckBox("未知的性别")
        self.unkonwn_gender.stateChanged.connect(self.gender_unkonwn)
        self.unscript_gender = QCheckBox("未说明的性别")
        self.unscript_gender.stateChanged.connect(self.gender_unscript)
        self.gender_layout = QGridLayout()
        self.gender_layout.addWidget(self.male,0,0)
        self.gender_layout.addWidget(self.unkonwn_gender,0,1)
        self.gender_layout.addWidget(self.female,1,0)
        self.gender_layout.addWidget(self.unscript_gender,1,1)
        self.gender_layout2 = QWidget()
        self.gender_layout2.setLayout(self.gender_layout)

        self.racelabel = QLabel('民族')
        self.race = QComboBox()
        self.race.setEditable(True)
        self.race.addItem('汉族')
        self.race.addItem('回族')
        self.race.addItem('蒙古族')
        self.race.addItem('壮族')
        self.race.addItem('藏族')
        self.race.addItem('维吾尔族')

        self.nationlabel = QLabel('国家或地区')
        self.nation = QLineEdit("中国")

        self.id_class_label = QLabel("有效身份证件类别")
        self.id_class = QComboBox()
        self.id_class.addItem("身份证")
        self.id_class.addItem("户口簿")
        self.id_class.addItem("护照")
        self.id_class.addItem("军官证")
        self.id_class.addItem("驾驶证")
        self.id_class.addItem("港澳通行证")
        self.id_class.addItem("台湾通行证")
        self.id_class.addItem("其他法定有效证件")

        self.idlabel = QLabel('证件号码')
        self.id = QLineEdit()
        self.id_bnt = QLabel('请按回车ENTER')
        self.id_press = QPushButton('->')
        self.id_press.clicked.connect(self.id_to_date)

        self.birthlable = QLabel('出生日期')
        self.birthday = QDateEdit()
        self.birthchoice = QPushButton()
        self.birthchoice.setStyleSheet('border:hidden;text-align:left')
        self.birthchoice.setIcon(QIcon('cal2.png'))
        self.birthchoice.clicked.connect(self.show_birth_cal)



        a = Address()
        a.location_label.setText("户籍详细地址")
        a.id_label.setText("户籍地址国标")
        self.address_now = a.location
        self.code_now = a.id
        b = Address()
        b.location_label.setText("死者生前详细地址")
        b.id_label.setText("死者生前常住地址国标")
        self.address_birth= b.location
        self.code_birth= b.id

        self.deathlabel = QLabel('死亡日期')
        self.deathdate = QDateEdit()
        self.deathchoice = QPushButton()
        self.deathchoice.setStyleSheet('border:hidden;text-align:left')
        self.deathchoice.setIcon(QIcon('cal2.png'))
        self.deathchoice.clicked.connect(self.show_death_cal)

        self.diseaselabel = QLabel('死因')
        self.disease = QLineEdit()

        self.regist_date_lable = QLabel('登记日期')
        self.regist_date = QDateEdit(QDate.currentDate())
        self.regist_date_choice = QPushButton()
        self.regist_date_choice.setStyleSheet('border:hidden;text-align:left;')
        self.regist_date_choice.setIcon(QIcon('cal2.png'))
        self.regist_date_choice.clicked.connect(self.show_regist_cal)

        self.familylabel = QLabel('家属姓名')
        self.family = QLineEdit()

        self.tellabel= QLabel('联系方式')
        self.tel = QLineEdit()

        self.layout.addWidget(self.number_label,0,0)
        self.layout.addWidget(self.number,0,1,1,2)
        self.layout.addWidget(self.birthlable,1,0)
        self.layout.addWidget(self.birthday,1,1,1,2)
        self.layout.addWidget(self.birthchoice,1,3)
        self.layout.addWidget(a,2,0,1,4)
        self.layout.addWidget(b,3,0,1,4)
        self.layout.addWidget(self.deathlabel,4,0)
        self.layout.addWidget(self.deathdate,4,1,1,2)
        self.layout.addWidget(self.deathchoice,4,3)
        self.layout.addWidget(self.genderlabel,5,0)
        self.layout.addWidget(self.gender_layout2,5,1,1,4)
        self.layout.addWidget(self.report_distinct_lable,9,0)
        self.layout.addWidget(self.report_distinct,9,1)
        self.layout.addWidget(self.report_depart_lable,9,2)
        self.layout.addWidget(self.report_department,9,3)


        self.back_bnt = QPushButton('返回(ESC)')
        self.back_bnt.clicked.connect(self.back_click)

        self.print_bnt = QPushButton('打印(F5)')
        self.print_bnt.clicked.connect(self.print_record)

        self.save_bnt = QPushButton('保存(F2)')
        self.save_bnt.clicked.connect(self.save_record)

        self.add_bnt = QPushButton('添加(F1)')
        self.add_bnt.clicked.connect(self.add_record)


        self.layout.addWidget(self.save_bnt,9,0)
        self.layout.addWidget(self.add_bnt,10,0)
        self.layout.addWidget(self.print_bnt,11,0)
        self.layout.addWidget(self.back_bnt,12,0)
        self.setLayout(self.layout)


    def back_click(self):
        pass

    def save_record(self):
        print(self.address_now.text())

    def print_record(self):
        pass

    def add_record(self):
        pass

    def gender_male(self, state):
        if state == Qt.Checked:
            self.gender.setText("男性")
            self.female.setChecked(False)
            self.unkonwn_gender.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_female(self, state):
        if state == Qt.Checked:
            self.gender.setText("女性")
            self.male.setChecked(False)
            self.unkonwn_gender.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_unkonwn(self, state):
        if state == Qt.Checked:
            self.gender.setText("未知的性别")
            self.male.setChecked(False)
            self.female.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_unscript(self, state):
        if state == Qt.Checked:
            self.gender.setText("未说明的性别")
            self.male.setChecked(False)
            self.unkonwn_gender.setChecked(False)
            self.female.setChecked(False)

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
                self.unkonw_gender.setChecked(False)
                self.unscript_gender.setChecked(False)
            else:
                self.female.setChecked(False)
                self.male.setChecked(True)
                self.unkonw_gender.setChecked(False)
                self.unscript_gender.setChecked(False)

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
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_birthday)

    def input_birthday(self, date):
        self.birthday.setDate(date)

    def show_death_cal(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_deathday)

    def input_deathday(self, date):
        self.deathdate.setDate(date)

    def show_regist_cal(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_registday)

    def input_registday(self, date):
        self.regist_date.setDate(date)







if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Regist()
        mainwindow.show()
        sys.exit(app.exec_())
