#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets
from address import *
from calendar import *
from login import *

class Regist(QWidget):

    def __init__(self, user):
        super(Regist,self).__init__()
        self.user = user
        self.setWindowTitle("登记")
        self.resize(600, 400)
        self.move(50, 50)
        self.set_ui()

    def set_ui(self):

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,2)
        self.layout.setColumnStretch(2,1)
        self.layout.setColumnStretch(3,2)

        self.title= QLabel("登        记")
        self.title.setStyleSheet('''font-size:40px;''')
        self.title.setAlignment(Qt.AlignCenter)

        self.report_distinct_label = QLabel("报告地区")
        self.report_distinct = QLineEdit()
        self.report_distinct.setReadOnly(True)

        self.report_depart_label = QLabel("报告单位")
        self.report_department = QLineEdit()

        self.number_label = QLabel('编号')
        self.number = QLineEdit()
        self.number2 = str(QDateTime.currentDateTime().toPyDateTime()).replace('/',
                            '').replace(' ','').replace(':','').replace('.','').replace('-','')[:-3]
        self.number.setPlaceholderText(self.number2)
        self.number.setReadOnly(True)

        self.name_label = QLabel('姓名')
        self.name = QLineEdit()

        self.gender_label = QLabel('性别')
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

        self.race_label = QLabel('民族')
        self.race = QComboBox()
        self.race.setEditable(True)
        self.race.addItem('汉族')
        self.race.addItem('回族')
        self.race.addItem('蒙古族')
        self.race.addItem('壮族')
        self.race.addItem('藏族')
        self.race.addItem('维吾尔族')

        self.nation_label = QLabel('国家或地区')
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

        self.id_label = QLabel('证件号码')
        self.id = QLineEdit()
        self.id.setClearButtonEnabled(True)
        self.id_bnt = QPushButton('点击生成日期、年龄')
        self.id_bnt.clicked.connect(self.id_to_date)

        self.birth_label = QLabel('出生日期')
        self.birthday = QDateEdit()
        self.birth_date_choose = QPushButton()
        self.birth_date_choose.setStyleSheet('border:hidden;text-align:left')
        self.birth_date_choose.setIcon(QIcon('cal2.png'))
        self.birth_date_choose.clicked.connect(self.show_birth_cal)

        self.age_label = QLabel("出生日期不详填年龄")
        self.age = QLineEdit()
        self.age_unit = QComboBox()
        self.age_unit.addItem("岁")
        self.age_unit.addItem('月')
        self.age_unit.addItem('天')

        self.marriage_label = QLabel("婚姻状况")
        self.marriage = QComboBox()
        self.marriage.addItem("未婚")
        self.marriage.addItem("已婚")
        self.marriage.addItem("丧偶")
        self.marriage.addItem("离婚")
        self.marriage.addItem("未说明")

        self.education_label = QLabel("文化程度")
        self.education = QComboBox()
        education_list = ['研究生','大学','大专','中专','技校','高中','初中及以下']
        for i in education_list:
            self.education.addItem(i)

        self.occup_label = QLabel("个人身份")
        self.occupation = QComboBox()
        occupation_list = ['公务员','专业技术人员','职员','企业管理者','工人','农民','学生','现役军人',
                            '自由职业者','个体经营者','无业人员','离退休人员','其他']
        for i in occupation_list:
            self.occupation.addItem(i)

        self.death_date_label = QLabel('死亡日期')
        # self.death_date = QDateEdit()
        self.death_date = QDateTimeEdit()
        self.death_date_choose= QPushButton()
        self.death_date_choose.setStyleSheet('border:hidden;text-align:left')
        self.death_date_choose.setIcon(QIcon('cal2.png'))
        self.death_date_choose.clicked.connect(self.show_death_cal)

        self.death_location_label = QLabel("死亡地点")
        self.death_location = QComboBox()
        death_location_list = ['医疗卫生机构','来院途中','家中','养老服务机构','其他场所','不详']
        for i in death_location_list:
            self.death_location.addItem(i)

        self.company_label = QLabel("死者生前工作单位")
        self.company = QLineEdit()
        self.company.setClearButtonEnabled(True)

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

        self.family_label = QLabel("可联系的家属姓名")
        self.family = QLineEdit()

        self.family_tel_label = QLabel("家属联系电话")
        self.family_tel = QLineEdit()

        self.family_address_label = QLabel("家属住址或工作单位")
        self.family_address = QLineEdit()
        self.family_address.setClearButtonEnabled(True)

        self.disease_label1 = QLabel("Ⅰ.直接导致死亡的疾病或情况")
        self.disease_a_label = QLabel("直接死亡原因（a）")
        self.disease_a = QLineEdit()
        self.disease_a_time = QLineEdit()
        self.disease_a_time.setPlaceholderText("请输入时间间隔")
        self.disease_a_time_unit = QComboBox()
        self.disease_a_time_unit.addItem("年")
        self.disease_a_time_unit.addItem("月")
        self.disease_a_time_unit.addItem("日")
        self.disease_a_time_unit.addItem("小时")

        self.disease_b_label = QLabel("直接死亡原因（b）")
        self.disease_b = QLineEdit()
        self.disease_b_time = QLineEdit()
        self.disease_b_time.setPlaceholderText("请输入时间间隔")
        self.disease_b_time_unit = QComboBox()
        self.disease_b_time_unit.addItem("年")
        self.disease_b_time_unit.addItem("月")
        self.disease_b_time_unit.addItem("日")
        self.disease_b_time_unit.addItem("小时")

        self.disease_c_label = QLabel("直接死亡原因（c）")
        self.disease_c = QLineEdit()
        self.disease_c_time = QLineEdit()
        self.disease_c_time.setPlaceholderText("请输入时间间隔")
        self.disease_c_time_unit = QComboBox()
        self.disease_c_time_unit.addItem("年")
        self.disease_c_time_unit.addItem("月")
        self.disease_c_time_unit.addItem("日")
        self.disease_c_time_unit.addItem("小时")

        self.disease_d_label = QLabel("直接死亡原因（d）")
        self.disease_d = QLineEdit()
        self.disease_d_time = QLineEdit()
        self.disease_d_time.setPlaceholderText("请输入时间间隔")
        self.disease_d_time_unit = QComboBox()
        self.disease_d_time_unit.addItem("年")
        self.disease_d_time_unit.addItem("月")
        self.disease_d_time_unit.addItem("日")
        self.disease_d_time_unit.addItem("小时")

        self.other_disease_label = QLabel("Ⅱ.其他疾病诊断")
        self.other_disease = QLineEdit()

        self.death_reason_label = QLabel("根本死亡原因")
        self.death_reason = QLineEdit()

        self.diagnost_depart_label = QLabel("最高诊断单位")
        self.diagnost_department = QComboBox()
        diagnost_department_list = ['三级医院','二级医院','乡镇卫生院或社区卫生服务中心','村卫生室','其他医疗卫生机构','未就诊']
        for i in diagnost_department_list:
            self.diagnost_department.addItem(i)

        self.diagnost_method_label = QLabel("最高诊断依据")
        self.diagnost_method = QComboBox()
        diagnost_method_list = ['尸检','病理','手术','临床+理化','临床','死后推断','不详']
        for i in diagnost_method_list:
            self.diagnost_method.addItem(i)

        self.inhospital_label = QLabel("住院号")
        self.inhospital = QLineEdit()

        self.doctor_label = QLabel("填卡医生")
        self.doctor = QLineEdit()

        self.regist_date_label = QLabel('医生填卡日期')
        self.regist_date = QDateEdit(QDate.currentDate())
        self.regist_date_choose= QPushButton()
        self.regist_date_choose.setStyleSheet('border:hidden;text-align:left;')
        self.regist_date_choose.setIcon(QIcon('cal2.png'))
        self.regist_date_choose.clicked.connect(self.show_regist_cal)

        self.reporter_label = QLabel('报告人')
        self.reporter = QLineEdit()
        self.reporter.setReadOnly(True)

        self.backup_label = QLabel("备注")
        self.backup = QLineEdit()

        self.research_label = QLabel("死者生前病史及症状体征")
        self.research = QTextEdit()

        self.researcher_label = QLabel("被调查者姓名")
        self.researcher = QLineEdit()

        self.relation_label = QLabel("与死者关系")
        self.relation = QLineEdit()

        self.researcher_address_label = QLabel("联系地址或工作单位")
        self.researcher_address = QLineEdit()

        self.researcher_tel_label = QLabel("被调查者电话号码")
        self.researcher_tel = QLineEdit()

        self.death_reason2_label = QLabel("死因推断")
        self.death_reason2 = QLineEdit()

        self.research_date_label = QLabel("调查日期")
        self.research_date= QDateEdit(QDate.currentDate())
        self.research_date_choose = QPushButton()
        self.research_date_choose.setStyleSheet('border:hidden;text-align:left;')
        self.research_date_choose.setIcon(QIcon('cal2.png'))
        self.research_date_choose.clicked.connect(self.show_research_cal)

        self.back_bnt = QPushButton('返回(ESC)')
        self.back_bnt.clicked.connect(self.back_click)

        self.print_bnt = QPushButton('打印(F5)')
        self.print_bnt.clicked.connect(self.print_record)

        self.save_bnt = QPushButton('保存(F2)')
        self.save_bnt.clicked.connect(self.save_record)

        self.add_bnt = QPushButton('添加(F1)')
        self.add_bnt.clicked.connect(self.add_record)

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout2 = QWidget()
        self.bnt_layout.addWidget(self.add_bnt)
        self.bnt_layout.addWidget(self.save_bnt)
        self.bnt_layout.addWidget(self.print_bnt)
        self.bnt_layout.addWidget(self.back_bnt)
        self.bnt_layout2.setLayout(self.bnt_layout)


        self.layout.addWidget(self.report_distinct_label,1,0)
        self.layout.addWidget(self.report_distinct,1,1)
        self.layout.addWidget(self.report_depart_label,1,2)
        self.layout.addWidget(self.report_department,1,3)
        self.layout.addWidget(self.number_label,2,0)
        self.layout.addWidget(self.number,2,1)
        self.layout.addWidget(self.name_label,3,0)
        self.layout.addWidget(self.name,3,1)
        self.layout.addWidget(self.gender_label,4,0)
        self.layout.addWidget(self.gender_layout2,4,1,1,2)
        self.layout.addWidget(self.race_label,5,0)
        self.layout.addWidget(self.race,5,1)
        self.layout.addWidget(self.nation_label,6,0)
        self.layout.addWidget(self.nation,6,1)
        self.layout.addWidget(self.id_class_label,7,0)
        self.layout.addWidget(self.id_class,7,1)
        self.layout.addWidget(self.id_label,8,0)
        self.layout.addWidget(self.id,8,1)
        self.layout.addWidget(self.id_bnt,8,2)
        self.layout.addWidget(self.birth_label,9,0)
        self.layout.addWidget(self.birthday,9,1)
        self.layout.addWidget(self.birth_date_choose,9,2)
        self.layout.addWidget(self.age_label,10,0)
        self.layout.addWidget(self.age,10,1)
        self.layout.addWidget(self.age_unit,10,2)
        self.layout.addWidget(self.marriage_label,11,0)
        self.layout.addWidget(self.marriage,11,1)
        self.layout.addWidget(self.education_label,12,0)
        self.layout.addWidget(self.education,12,1)
        self.layout.addWidget(self.occup_label,13,0)
        self.layout.addWidget(self.occupation,13,1)
        self.layout.addWidget(self.death_date_label,14,0)
        self.layout.addWidget(self.death_date,14,1)
        self.layout.addWidget(self.death_date_choose,14,2)
        self.layout.addWidget(self.death_location_label,15,0)
        self.layout.addWidget(self.death_location,15,1)
        self.layout.addWidget(self.company_label,16,0)
        self.layout.addWidget(self.company,16,1)
        self.layout.addWidget(a,17,0,1,4)
        self.layout.addWidget(b,18,0,1,4)
        self.layout.addWidget(self.family_label,19,0)
        self.layout.addWidget(self.family,19,1)
        self.layout.addWidget(self.family_tel_label,20,0)
        self.layout.addWidget(self.family_tel,20,1)
        self.layout.addWidget(self.family_address_label,21,0)
        self.layout.addWidget(self.family_address,21,1)
        self.layout.addWidget(self.disease_label1,22,0)
        self.layout.addWidget(self.disease_a_label,23,0)
        self.layout.addWidget(self.disease_a,23,1)
        self.layout.addWidget(self.disease_a_time,23,2)
        self.layout.addWidget(self.disease_a_time_unit,23,3)
        self.layout.addWidget(self.disease_b_label,24,0)
        self.layout.addWidget(self.disease_b,24,1)
        self.layout.addWidget(self.disease_b_time,24,2)
        self.layout.addWidget(self.disease_b_time_unit,24,3)
        self.layout.addWidget(self.disease_c_label,25,0)
        self.layout.addWidget(self.disease_c,25,1)
        self.layout.addWidget(self.disease_c_time,25,2)
        self.layout.addWidget(self.disease_c_time_unit,25,3)
        self.layout.addWidget(self.disease_d_label,26,0)
        self.layout.addWidget(self.disease_d,26,1)
        self.layout.addWidget(self.disease_d_time,26,2)
        self.layout.addWidget(self.disease_d_time_unit,26,3)
        self.layout.addWidget(self.other_disease_label,30,0)
        self.layout.addWidget(self.other_disease,30,1)
        self.layout.addWidget(self.death_reason_label,32,0)
        self.layout.addWidget(self.death_reason,32,1)
        self.layout.addWidget(self.diagnost_depart_label,33,0)
        self.layout.addWidget(self.diagnost_department,33,1)
        self.layout.addWidget(self.diagnost_method_label,34,0)
        self.layout.addWidget(self.diagnost_method,34,1)
        self.layout.addWidget(self.inhospital_label,35,0)
        self.layout.addWidget(self.inhospital,35,1)
        self.layout.addWidget(self.doctor_label,36,0)
        self.layout.addWidget(self.doctor,36,1)
        self.layout.addWidget(self.regist_date_label,37,0)
        self.layout.addWidget(self.regist_date,37,1)
        self.layout.addWidget(self.regist_date_choose,37,2)
        self.layout.addWidget(self.reporter_label,38,0)
        self.layout.addWidget(self.reporter,38,1)
        self.layout.addWidget(self.backup_label,39,0)
        self.layout.addWidget(self.backup,39,1)
        self.layout.addWidget(self.research_label,40,0)
        self.layout.addWidget(self.research,40,1,3,4)
        self.layout.addWidget(self.researcher_label,44,0)
        self.layout.addWidget(self.researcher,44,1)
        self.layout.addWidget(self.relation_label,44,2)
        self.layout.addWidget(self.relation,44,3)
        self.layout.addWidget(self.researcher_address_label,45,0)
        self.layout.addWidget(self.researcher_address,45,1)
        self.layout.addWidget(self.researcher_tel_label,45,2)
        self.layout.addWidget(self.researcher_tel,45,3)
        self.layout.addWidget(self.death_reason2_label,46,0)
        self.layout.addWidget(self.death_reason2,46,1)
        self.layout.addWidget(self.research_date_label,47,0)
        self.layout.addWidget(self.research_date,47,1)
        self.layout.addWidget(self.research_date_choose,47,2)


        self.layout.addWidget(self.bnt_layout2,50,0,1,4)

        # self.setLayout(self.layout)

        self.scroll = QScrollArea(self)
        self.scroll.setAutoFillBackground(True)
        self.scroll.setMinimumSize(800,600)
        self.scroll.setWidgetResizable(True)
        self.scroll_bar = self.scroll.verticalScrollBar()

        self.layout2 = QWidget()
        self.layout2.setLayout(self.layout)

        self.scroll.setWidget(self.layout2)

        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.title)
        self.layout3.addWidget(self.scroll)

        self.setLayout(self.layout3)
        # self.setLayout(self.scroll)



    def back_click(self):
        self.close()
        self.listwindow = ListWindow(self.user)
        self.listwindow.show()

    def save_record(self):
        print(self.address_now.text())

    def print_record(self):
        self.a = QWebEngineView()
        self.a.load(QUrl('https://baidu.com'))
        self.a.show()

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
                self.unkonwn_gender.setChecked(False)
                self.unscript_gender.setChecked(False)
            else:
                self.female.setChecked(False)
                self.male.setChecked(True)
                self.unkonwn_gender.setChecked(False)
                self.unscript_gender.setChecked(False)

            certify_number = ['1','0','X','9','8','7','6','5','4','3','2','1']
            std_number = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
            sum = 0
            for i in range(17):
                sum += int(id_upper[i])*std_number[i]
            certify_rslt = certify_number[sum%11]
            if certify_rslt != id_upper[-1]:
                self.id_bnt.setText('身份证号码不正确')
                self.id_bnt.setStyleSheet('color:red')
            else:
                self.id_bnt.setText('请点击')
        else:
            self.id_bnt.setText('未满18位')

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
        self.death_date.setDate(date)

    def show_regist_cal(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_registday)

    def input_registday(self, date):
        self.regist_date.setDate(date)

    def show_research_cal(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_researchday)

    def input_researchday(self, date):
        self.research_date.setDate(date)
