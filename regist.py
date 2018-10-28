#!/usr/bin/env python
#coding: utf-8

import login
from address import *
from calendar import *
import address_dic
from data import *
from printwindow import *
import datetime

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

        list_dic = Choice_Dic()

        self.db = DataBase()
        self.db.cur.execute("select a.*,b.* from user as a, hospital as b where a.hospital_id = b.id and a.username = '%s'"%(self.user))
        rslt = self.db.cur.fetchall()[0]
        self.hospital_id = rslt[3]
        self.distinct_code = str(rslt[8])
        # self.db.cur.execute("select * from race")
        # race_rslt = self.db.cur.fetchall()
        self.db.cur.execute("select name from hospital")
        hospital_rslt = self.db.cur.fetchall()
        self.db.con.close()

        self.title= QLabel("登        记")
        self.title.setStyleSheet('''font-size:40px;''')
        self.title.setAlignment(Qt.AlignCenter)

        self.report_distinct_label = QLabel("报告地区")
        self.report_distinct = QLineEdit()
        self.report_distinct.setReadOnly(True)

        self.report_depart_label = QLabel("报告单位")
        # self.report_department = QLineEdit()
        self.report_department = QComboBox()
        for i in hospital_rslt:
            self.report_department.addItem(i[0])

        self.serial_number_label = QLabel('编号')
        self.serial_number = QLineEdit()
        self.number2 = str(QDateTime.currentDateTime().toPyDateTime()).replace('/',
                            '').replace(' ','').replace(':','').replace('.','').replace('-','')[:-3]
        self.serial_number.setPlaceholderText(self.number2)
        self.serial_number.setReadOnly(True)
        self.bianhao_label = QLabel("死亡卡编号")
        self.bianhao = QLineEdit()
        self.bianhao.setReadOnly(True)

        self.name_label = QLabel('姓名')
        self.name = QLineEdit()

        self.gender_label = QLabel('性别')
        # self.gender = QLineEdit()
        self.gender_code = QLineEdit()
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
        race_rslt = list_dic.race_list
        for i in race_rslt:
            self.race.addItem(i)

        self.nation_label = QLabel('国家或地区')
        self.nation = QLineEdit("中国")

        self.id_class_label = QLabel("有效身份证件类别")
        self.id_class = QComboBox()
        id_class_list = list_dic.id_class_list
        for i in id_class_list:
            self.id_class.addItem(i)

        self.id_label = QLabel('证件号码')
        self.id = QLineEdit()
        self.id.setClearButtonEnabled(True)
        self.id_bnt = QPushButton('点击生成日期、性别')
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
        self.age_generate_bnt = QPushButton("点击生成年龄")
        self.age_generate_bnt.clicked.connect(self.generate_age)
        age_unit_list = list_dic.age_unit
        age_unit_list2 = ['岁','月','天']
        for i in age_unit_list2:
            self.age_unit.addItem(i)

        self.marriage_label = QLabel("婚姻状况")
        self.marriage = QComboBox()
        marriage_list = list_dic.marriage_list
        for i in marriage_list:
            self.marriage.addItem(i)

        self.education_label = QLabel("文化程度")
        self.education = QComboBox()
        education_list = list_dic.education_list
        for i in education_list:
            self.education.addItem(i)

        self.occup_label = QLabel("个人身份")
        self.occupation = QComboBox()
        occupation_list = list_dic.occupation_list
        for i in occupation_list:
            self.occupation.addItem(i)

        self.death_date_label = QLabel('死亡日期')
        self.death_date = QDateTimeEdit()
        self.death_date_choose= QPushButton()
        self.death_date_choose.setStyleSheet('border:hidden;text-align:left')
        self.death_date_choose.setIcon(QIcon('cal2.png'))
        self.death_date_choose.clicked.connect(self.show_death_cal)

        self.death_location_label = QLabel("死亡地点")
        self.death_location = QComboBox()
        death_location_list = list_dic.death_location_list
        for i in death_location_list:
            self.death_location.addItem(i)

        self.company_label = QLabel("死者生前工作单位")
        self.company = QLineEdit()
        self.company.setClearButtonEnabled(True)

        address_a = Address()
        address_a.province.setCurrentText(address_dic.province_dic[self.distinct_code[:2]])
        address_a.city.setCurrentText(address_dic.city_dic[self.distinct_code[:2]][self.distinct_code[:4]])
        address_a.county.setCurrentText(address_dic.county_dic[self.distinct_code[:4]][self.distinct_code[:6]])
        address_a.location_label.setText("户籍详细地址")
        address_a.id_label.setText("户籍地址国标")
        self.address_now = address_a.location
        self.code_now = address_a.id

        address_b = Address()
        address_b.province.setCurrentText(address_dic.province_dic[self.distinct_code[:2]])
        address_b.city.setCurrentText(address_dic.city_dic[self.distinct_code[:2]][self.distinct_code[:4]])
        address_b.county.setCurrentText(address_dic.county_dic[self.distinct_code[:4]][self.distinct_code[:6]])
        address_b.location_label.setText("死者生前详细地址")
        address_b.id_label.setText("死者生前常住地址国标")
        self.address_birth= address_b.location
        self.code_birth= address_b.id

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
        for i in age_unit_list:
            self.disease_a_time_unit.addItem(i)

        self.disease_b_label = QLabel("直接死亡原因（b）")
        self.disease_b = QLineEdit()
        self.disease_b_time = QLineEdit()
        self.disease_b_time.setPlaceholderText("请输入时间间隔")
        self.disease_b_time_unit = QComboBox()
        for i in age_unit_list:
            self.disease_b_time_unit.addItem(i)

        self.disease_c_label = QLabel("直接死亡原因（c）")
        self.disease_c = QLineEdit()
        self.disease_c_time = QLineEdit()
        self.disease_c_time.setPlaceholderText("请输入时间间隔")
        self.disease_c_time_unit = QComboBox()
        for i in age_unit_list:
            self.disease_c_time_unit.addItem(i)

        self.disease_d_label = QLabel("直接死亡原因（d）")
        self.disease_d = QLineEdit()
        self.disease_d_time = QLineEdit()
        self.disease_d_time.setPlaceholderText("请输入时间间隔")
        self.disease_d_time_unit = QComboBox()
        for i in age_unit_list:
            self.disease_d_time_unit.addItem(i)

        self.other_disease_label = QLabel("Ⅱ.其他疾病诊断")
        self.other_disease = QLineEdit()

        self.death_reason_label = QLabel("根本死亡原因")
        self.death_reason = QLineEdit()

        self.icd10_label = QLabel("ICD10编码")
        self.icd10 = QLineEdit()

        self.diagnost_depart_label = QLabel("最高诊断单位")
        self.diagnost_department = QComboBox()
        diagnost_department_list = list_dic.diagnost_department_list
        for i in diagnost_department_list:
            self.diagnost_department.addItem(i)

        self.diagnost_method_label = QLabel("最高诊断依据")
        self.diagnost_method = QComboBox()
        diagnost_method_list = list_dic.diagnost_method_list
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

        self.print_page_bnt = QPushButton('打印(F5)')
        self.print_page_bnt.clicked.connect(self.print_page)

        self.save_bnt = QPushButton('保存(ENT)')
        self.save_bnt.clicked.connect(self.save_record)

        self.add_bnt = QPushButton('添加(F1)')
        self.add_bnt.clicked.connect(self.add_record)

        self.doctor.setText(rslt[1])
        self.report_distinct_code = str(rslt[8])
        report_distinct_name = address_dic.county_dic[self.report_distinct_code[:4]][self.report_distinct_code[:6]]
        self.report_distinct.setText(report_distinct_name)
        self.report_department.setCurrentText(rslt[7])
        self.reporter.setText(rslt[-1])

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout2 = QWidget()
        self.bnt_layout.addWidget(self.add_bnt)
        self.bnt_layout.addWidget(self.save_bnt)
        self.bnt_layout.addWidget(self.print_page_bnt)
        self.bnt_layout.addWidget(self.back_bnt)
        self.bnt_layout2.setLayout(self.bnt_layout)

        self.layout.addWidget(self.report_distinct_label,1,0)
        self.layout.addWidget(self.report_distinct,1,1)
        self.layout.addWidget(self.report_depart_label,1,2)
        self.layout.addWidget(self.report_department,1,3)
        self.layout.addWidget(self.serial_number_label,2,0)
        self.layout.addWidget(self.serial_number,2,1)
        self.layout.addWidget(self.bianhao_label,2,2)
        self.layout.addWidget(self.bianhao,2,3)
        self.layout.addWidget(self.name_label,3,0)
        self.layout.addWidget(self.name,3,1)
        self.layout.addWidget(self.id_class_label,4,0)
        self.layout.addWidget(self.id_class,4,1)
        self.layout.addWidget(self.id_label,5,0)
        self.layout.addWidget(self.id,5,1)
        self.layout.addWidget(self.id_bnt,5,2)
        self.layout.addWidget(self.gender_label,6,0)
        self.layout.addWidget(self.gender_layout2,6,1,1,2)
        self.layout.addWidget(self.race_label,7,0)
        self.layout.addWidget(self.race,7,1)
        self.layout.addWidget(self.nation_label,8,0)
        self.layout.addWidget(self.nation,8,1)
        self.layout.addWidget(self.birth_label,9,0)
        self.layout.addWidget(self.birthday,9,1)
        self.layout.addWidget(self.birth_date_choose,9,2)
        self.layout.addWidget(self.death_date_label,10,0)
        self.layout.addWidget(self.death_date,10,1)
        self.layout.addWidget(self.death_date_choose,10,2)
        self.layout.addWidget(self.age_label,11,0)
        self.layout.addWidget(self.age,11,1)
        self.layout.addWidget(self.age_unit,11,2)
        self.layout.addWidget(self.age_generate_bnt,11,3)
        self.layout.addWidget(self.marriage_label,12,0)
        self.layout.addWidget(self.marriage,12,1)
        self.layout.addWidget(self.education_label,13,0)
        self.layout.addWidget(self.education,13,1)
        self.layout.addWidget(self.occup_label,14,0)
        self.layout.addWidget(self.occupation,14,1)
        self.layout.addWidget(self.death_location_label,15,0)
        self.layout.addWidget(self.death_location,15,1)
        self.layout.addWidget(self.company_label,16,0)
        self.layout.addWidget(self.company,16,1)
        self.layout.addWidget(address_a,17,0,1,4)
        self.layout.addWidget(address_b,18,0,1,4)
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
        self.layout.addWidget(self.icd10_label,32,2)
        self.layout.addWidget(self.icd10,32,3)
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
        self.layout3.addWidget(self.bnt_layout2)

        self.setLayout(self.layout3)

    def back_click(self):
        self.close()
        from login import ListWindow
        self.listwindow = ListWindow(self.user)
        self.listwindow.show()

    def get_bianhao(self):
        self.db = DataBase()
        self.db.cur.execute("select hospital_id from user where username = '%s'"%(self.user))
        hospital_id = self.db.cur.fetchone()[0]
        self.db.cur.execute("select * from bianhao where hospital_id = %d"%(hospital_id))
        rslt = self.db.cur.fetchone()
        year_now = datetime.datetime.now().year
        if year_now > rslt[2]:
            year = year_now
            last_number = 1
        else:
            year = rslt[2]
            last_number = rslt[3] + 1
        self.db.cur.execute('select depart_code from hospital where id = %d'%(hospital_id))
        depart_code = self.db.cur.fetchone()[0]
        self.db.con.close()
        return [depart_code, year, last_number, hospital_id]

    def print_page(self):
        self.a = PrintWindow(self.serial_number.text(), 1)
        self.a.show()

    def gender_male(self, state):
        if state == Qt.Checked:
            self.gender_code.setText('1')
            self.female.setChecked(False)
            self.unkonwn_gender.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_female(self, state):
        if state == Qt.Checked:
            self.gender_code.setText('2')
            self.male.setChecked(False)
            self.unkonwn_gender.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_unkonwn(self, state):
        if state == Qt.Checked:
            self.gender_code.setText('3')
            self.male.setChecked(False)
            self.female.setChecked(False)
            self.unscript_gender.setChecked(False)

    def gender_unscript(self, state):
        if state == Qt.Checked:
            self.gender_code.setText('4')
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

    def generate_age(self):
        if self.death_date != '':
            death_date = self.death_date.date().toPyDate()
            birth_date = self.birthday.date().toPyDate()
            date_delta = death_date - birth_date
            day_delta = date_delta.days
            if day_delta < 30:
                self.age.setText(str(day_delta))
                self.age_unit.setCurrentText("天")
            elif day_delta < 365.26:
                self.age.setText(str(round(day_delta//30)))
                self.age_unit.setCurrentText("月")
            else:
                self.age.setText(str(round(day_delta//365.25)))
                self.age_unit.setCurrentText("岁")
        else:
            self.age_generate_bnt.setText("死亡日期未填写")

    def show_birth_cal(self):
        self.cal = Calendar()
        self.cal.show()
        self.cal.date_signal.connect(self.input_birthday)

    def input_birthday(self, date):
        self.birthday.setDate(date)

    def show_death_cal(self):
        self.cal = Calendar_With_Clock()
        self.cal.show()
        self.cal.datetime_signal.connect(self.input_deathday)

    def input_deathday(self, datetime):
        self.death_date.setDateTime(datetime)

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

    def change_date(self,pyqtdate):   # a pyqtdate style /yyyymmdd to time stamp
        pydate = pyqtdate.date().toPyDate()
        base_date = datetime.date(1970,1,1)
        day_delta = pydate - base_date
        days = day_delta.days
        seconds = days*24*3600
        return seconds

    def change_datetime(self,pyqtdatetime):   # a pyqtdate style /yyyymmdd to time stamp
        pydate = pyqtdatetime.dateTime().toPyDateTime()
        base_date = datetime.datetime(1970,1,1,0,0)
        day_delta = pydate - base_date
        days = day_delta.days
        seconds = day_delta.seconds
        seconds += days*24*3600
        return seconds

    def change_time(self, time_text): # disease time to integer
        try:
            a = int(time_text)
        except ValueError:
            a = 0
        return a

    def save_record(self):
        bianhao_list = self.get_bianhao()
        bianhao = str(bianhao_list[0]) + str(bianhao_list[1]) + str(bianhao_list[2]).zfill(4)
        age = self.age.text() + self.age_unit.currentText()

        self.db = DataBase()
        data = (0,self.report_distinct_code,self.report_department.currentText(), self.number2,bianhao,
                self.name.text(),self.gender_code.text(),self.race.currentIndex(),self.nation.text(),self.id_class.currentIndex(),
                self.id.text(),self.change_date(self.birthday),age,self.marriage.currentIndex(),self.education.currentIndex(),
                self.occupation.currentIndex(),self.address_now.text(),self.code_now.text(),self.address_birth.text(),
                self.code_birth.text(),self.death_location.currentIndex(),self.company.text(),self.change_datetime(self.death_date),
                self.family.text(),self.family_tel.text(),self.family_address.text(),self.disease_a.text(),self.disease_a_time.text(),
                self.disease_a_time_unit.currentText(),self.disease_b.text(),self.disease_b_time.text(),self.disease_b_time_unit.currentText(),
                self.disease_c.text(),self.disease_c_time.text(),self.disease_c_time_unit.currentText(),
                self.disease_d.text(),self.disease_d_time.text(),self.disease_d_time_unit.currentText(),self.other_disease.text(),
                self.death_reason.text(),self.icd10.text().upper(),self.diagnost_department.currentIndex(),self.diagnost_method.currentIndex(),
                self.inhospital.text(),self.doctor.text(),self.change_date(self.regist_date),self.reporter.text(),self.hospital_id,
                self.backup.text(),self.research.toPlainText(),self.researcher.text(),self.relation.text(),
                self.researcher_address.text(),self.researcher_tel.text(),self.death_reason2.text(),self.change_date(self.research_date),0,0
                )
        insert_sql = '''INSERT INTO death_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
               '''
        if self.save_bnt.text() == "保存(ENT)":
            self.db.cur.execute("update bianhao set last_year = %d, last_number = %d where hospital_id = %d"%(bianhao_list[1], bianhao_list[2], bianhao_list[3]))
            self.db.cur.execute(insert_sql, data)
            self.save_bnt.setText("更新(ENT)")
            self.save_bnt.clicked.disconnect(self.save_record)
            self.save_bnt.clicked.connect(self.update_record)
        else:
            pass
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()

    def update_record(self):
        age = self.age.text() + self.age_unit.currentText()
        self.db = DataBase()
        update_sql = '''UPDATE death_info SET bianhao = '{0}',
            name = '{1}',
            gender_code = {2},
            race_code = {3},
            id_class = '{4}',
            id = '{5}',
            birthday = {6},
            age = '{7}',
            marriage_code = {8},
            education_code = {9},
            occupation_code = {10},
            address_now = '{11}',
            code_now = {12},
            address_birth = '{13}',
            code_birth = {14},
            death_location_code = {15},
            company = '{16}',
            death_date = {17},
            family = '{18}',
            family_tel = '{19}',
            family_address = '{20}',
            disease_a = '{21}',
            disease_a_time = {22},
            disease_a_time_unit = '{23}',
            disease_b = '{24}',
            disease_b_time = {25},
            disease_b_time_unit = '{26}',
            disease_c = '{27}',
            disease_c_time = {28},
            disease_c_time_unit = '{29}',
            disease_d = '{30}',
            disease_d_time = {31},
            disease_d_time_unit = '{32}',
            other_disease = '{33}',
            death_reason = '{34}',
            diagnost_department_code = {35},
            diagnost_method_code = {36},
            inhospital = '{37}',
            doctor = '{38}',
            regist_date = {39},
            backup = '{40}',
            research = '{41}',
            researcher = '{42}',
            relation = '{43}',
            researcher_address = '{44}',
            researcher_tel = '{45}',
            death_reason2 = '{46}',
            research_date = {47},
            icd10 = '{48}',
            nation = '{49}' where serial_number = "{50}"
            '''.format(self.bianhao.text(),
                self.name.text(),self.gender_code.text(),self.race.currentIndex(),self.id_class.currentIndex(),
                self.id.text(),self.change_date(self.birthday),age,self.marriage.currentIndex(),self.education.currentIndex(),
                self.occupation.currentIndex(),self.address_now.text(),self.code_now.text(),self.address_birth.text(),
                self.code_birth.text(),self.death_location.currentIndex(),self.company.text(),self.change_date(self.death_date),
                self.family.text(),self.family_tel.text(),self.family_address.text(),self.disease_a.text(),self.change_time(self.disease_a_time.text()),
                self.disease_a_time_unit.currentText(),self.disease_b.text(),self.disease_b_time.text(),self.disease_b_time_unit.currentText(),
                self.disease_c.text(),self.change_time(self.disease_c_time.text()),self.disease_c_time_unit.currentText(),
                self.disease_d.text(),self.change_time(self.disease_d_time.text()),self.disease_d_time_unit.currentText(),self.other_disease.text(),
                self.death_reason.text(),self.diagnost_department.currentIndex(),self.diagnost_method.currentIndex(),
                self.inhospital.text(),self.doctor.text(),self.change_date(self.regist_date),
                self.backup.text(),self.research.toPlainText(),self.researcher.text(),self.relation.text(),
                self.researcher_address.text(),self.researcher_tel.text(),self.death_reason2.text(),
                self.change_date(self.research_date),self.icd10.text().upper(),self.nation.text(),self.serial_number.text()
                )
        self.db.cur.execute(update_sql)
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()

    def add_record(self):
        self.save_record()
        self.close()
        self.new = Regist(self.user)
        self.new.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.save_record()

    def mousePressEvent(self, e):
        if e.buttons() == Qt.MiddleButton:
            pass
