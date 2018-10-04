#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets
from data import *
from calendar import *
from printwindow import *
from math import ceil
import address_dic
import regist
import login
import datetime

class QueryWindow(QWidget):

    def __init__(self, user):
        super(QueryWindow, self).__init__()
        self.user = user
        self.setWindowTitle("查询")
        # self.setFixedSize(1080, 800)
        self.resize(1200,800)
        self.set_ui()

    def set_ui(self):
        self.db = DataBase()
        self.db.cur.execute("select hospital_id from user where username = '%s'"%(self.user))
        hospital_id = self.db.cur.fetchone()[0]
        # self.db.cur.execute("select count(*) from death_info where hospital_code = '%s'"%(hospital_id))
        # rslt = self.db.cur.fetchone()
        # # amount = rslt[0]
        # pages = ceil(amount / 20)
        self.db.cur.execute("select name from hospital")
        hospital = self.db.cur.fetchall()
        self.db.con.close()
        hospital_list = [i[0] for i in hospital]
        self.name_label = QLabel("姓    名")
        self.name = QLineEdit()
        self.begin_date_label = QLabel("起始日期")
        self.begin_date = QDateEdit()
        self.begin_date_bnt = QPushButton()
        self.begin_date_bnt.setStyleSheet("border:hidden;")
        self.begin_date_bnt.setIcon(QIcon('cal2.png'))
        self.begin_date_bnt.clicked.connect(self.begin_date_choose)
        self.end_date_label = QLabel("截止日期")
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date_bnt = QPushButton()
        self.end_date_bnt.setStyleSheet("border:hidden;")
        self.end_date_bnt.setIcon(QIcon('cal2.png'))
        self.end_date_bnt.clicked.connect(self.end_date_choose)
        self.department_label = QLabel("单    位")
        self.department = QComboBox()
        for i in hospital_list:
            self.department.addItem(i)
        self.all_record = QRadioButton("所有记录")
        self.unreported_record= QRadioButton("未上报")
        self.unreported_record.setChecked(True)
        self.undeleted_record= QRadioButton("所有记录(含删除)")
        self.by_report_date = QRadioButton("按报告日期")
        self.by_report_date.setChecked(True)
        self.by_death_date = QRadioButton("按死亡日期")

        self.query_bnt = QPushButton("查询")
        self.requery_bnt = QPushButton("重置")
        self.export_bnt = QPushButton("导出Excel")
        self.close_bnt = QPushButton("关闭")
        self.query_bnt.clicked.connect(lambda:self.query_record())
        self.requery_bnt.clicked.connect(self.clear_click)
        self.export_bnt.clicked.connect(self.export_record)
        self.close_bnt.clicked.connect(self.close_window)
        self.query_bnt.setStyleSheet("background-color:green;border:hidden;color:white;text-align:center;width:30px;height:50px;")
        self.requery_bnt.setStyleSheet("background-color:blue;border:hidden;color:white;text-align:center;width:30px;height:50px;")
        self.export_bnt.setStyleSheet("background-color:violet;border:hidden;color:white;text-align:center;width:30px;height:50px;")
        self.close_bnt.setStyleSheet("background-color:red;border:hidden;color:white;text-align:center;width:30px;height:50px;")

        self.pre_page = QPushButton("前一页")
        self.next_page = QPushButton("后一页")
        self.page_info = QLabel()
        self.present_page = 1
        self.max_page = 1
        self.pre_page.clicked.connect(self.to_pre_page)
        self.next_page.clicked.connect(self.to_next_page)

        self.table = QTableWidget(20,12)
        # self.table.resizeColumnToContents(i)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,40)
        self.table.setColumnWidth(3,150)
        self.table.setColumnWidth(5,250)
        self.table.setColumnWidth(11,150)

        self.choose_record_layout = QHBoxLayout()
        self.choose_date_layout = QHBoxLayout()
        self.choose_record_layout.addWidget(self.all_record)
        self.choose_record_layout.addWidget(self.unreported_record)
        self.choose_record_layout.addWidget(self.undeleted_record)
        self.choose_date_layout.addWidget(self.by_report_date)
        self.choose_date_layout.addWidget(self.by_death_date)
        self.choose_record_layout2 = QWidget()
        self.choose_date_layout2 = QWidget()
        self.choose_record_layout2.setLayout(self.choose_record_layout)
        self.choose_date_layout2.setLayout(self.choose_date_layout)

        self.page_layout = QHBoxLayout()
        self.page_layout.addWidget(self.pre_page)
        self.page_layout.addWidget(self.page_info)
        self.page_layout.addWidget(self.next_page)

        self.page_layout2 = QWidget()
        self.page_layout2.setLayout(self.page_layout)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.name_label,0,0)
        self.head_layout.addWidget(self.name,0,1,1,2)
        self.head_layout.addWidget(self.department_label,0,4)
        self.head_layout.addWidget(self.department,0,5,1,2)
        self.head_layout.addWidget(self.begin_date_label,1,0)
        self.head_layout.addWidget(self.begin_date,1,1,1,2)
        self.head_layout.addWidget(self.begin_date_bnt,1,3)
        self.head_layout.addWidget(self.end_date_label,1,4)
        self.head_layout.addWidget(self.end_date,1,5,1,2)
        self.head_layout.addWidget(self.end_date_bnt,1,7)
        self.head_layout.addWidget(self.choose_record_layout2,2,0,1,2)
        self.head_layout.addWidget(self.choose_date_layout2,2,3,1,2)
        self.head_layout.addWidget(self.page_layout2,2,5,1,2)

        self.head_layout_main = QWidget()
        self.head_layout_main.setLayout(self.head_layout)

        self.bnt_layout = QGridLayout()
        self.bnt_layout.addWidget(self.query_bnt,0,0)
        self.bnt_layout.addWidget(self.export_bnt,0,1)
        self.bnt_layout.addWidget(self.requery_bnt,1,0)
        self.bnt_layout.addWidget(self.close_bnt,1,1)

        self.bnt_layout2 = QWidget()
        self.bnt_layout2.setLayout(self.bnt_layout)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.head_layout_main,0,0,1,7)
        self.main_layout.addWidget(self.bnt_layout2,0,7,1,1)
        self.main_layout.addWidget(self.table,3,0,5,8)

        self.setLayout(self.main_layout)

    def query_record(self,start = 0, numbers = 20):
        self.db = DataBase()
        self.db.cur.execute('select a.account_level, b.name from user as a, hospital as b where a.hospital_id = b.id and a.username = "%s"'%(self.user))
        rslt = self.db.cur.fetchone()
        if rslt[0] == 9:
            if self.department.currentText() == 'admin':
                department_sql = ''
            else:
                department_sql = ' and death_info.report_department = "%s"'%(self.department.currentText())
        else:
            department_sql = ' and death_info.report_department = "%s"'%(rslt[1])

        self.numbers =  numbers
        self.start = start
        if self.name.text() == '':
            name_sql = ' and death_info.name like "%"'
        else:
            name_text = '%' + self.name.text() + '%'
            name_sql = ' and death_info.name like "%s"'%(name_text)

        if self.all_record.isChecked():
            is_deleted_sql = ' and death_info.is_deleted = 0'
        elif self.undeleted_record.isChecked():
            is_deleted_sql = ' and death_info.is_deleted < 2 '
        else:
            is_deleted_sql = ' and death_info.is_reported = 0 and death_info.is_deleted = 0'
        if self.by_death_date.isChecked():
            date_sql = 'death_info.death_date'
        else:
            date_sql = 'death_info.regist_date'
        begin_date_interge = self.change_date(self.begin_date)
        end_date_interge = self.change_date(self.end_date)
        sql = '''
            select death_info.serial_number,death_info.name,gender.gender_name,death_info.id,death_info.birthday,death_info.address_now,death_info.death_date,
            death_info.disease_a,
            death_info.doctor, death_info.regist_date, death_info.report_department,death_info.is_deleted, death_info.is_reported from death_info,gender
            where death_info.gender_code = gender.gender_serial and date_conditon between %d and %d
        '''%(begin_date_interge,end_date_interge)

        number_sql = 'select count(*) from death_info where date_conditon between %d and %d '%(begin_date_interge,end_date_interge)
        # if self.id.text() != "":
            # sql2 = 'select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where id = %s limit %d offset %d'%(self.id.text(),self.numbers, self.start)
            # sql3 = 'select count(*) from base where id = %s '%(self.id.text())
        # else:
        sql2 = sql.replace('date_conditon',date_sql) +department_sql + is_deleted_sql + name_sql + '  limit %d offset %d'%(self.numbers,self.start)
        sql3 = number_sql.replace('date_conditon',date_sql) +department_sql + is_deleted_sql + name_sql         # sql3 = number_sql.replace('date2',date_sql) + is_deleted_sql + name_sql
        rlst_exec = self.db.cur.execute(sql2)
        rslt =  rlst_exec.fetchall()
        count1 = self.db.cur.execute(sql3).fetchone()
        count = count1[0]
        pages = ceil(count/self.numbers)
        pages_text = '共' + str(count) +'条 ' + str(pages) + '页，第' + str(self.present_page) +'页'
        self.page_info.setText(pages_text)
        self.max_page = pages
        k = 0
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['编号','姓名','性别','证件号码','出生日期','现住址','死亡日期','直接死因','报卡医生','报告日期','报告单位','操作'])
        for i in rslt:
            for j in range(11):
                if j in [4,6,9]:
                    self.table.setItem(k,j,QTableWidgetItem(self.to_date(i[j])))
                else:
                    self.table.setItem(k,j,QTableWidgetItem(str(i[j])))
            self.table.setCellWidget(k,11,self.button_row(i[0]))
            k += 1
        self.db.con.close()

    def button_row(self, id):
        self.db = DataBase()
        self.widget = QWidget()
        self.query_id = id
        self.view_bnt = QPushButton('查看')
        self.del_bnt = QPushButton('删除')
        self.regret_bnt = QPushButton('恢复')
        self.print_bnt = QPushButton('打印')
        self.report_bnt = QPushButton("上报")

        self.view_bnt.setStyleSheet('''text-align:center; background-color:green;border-style:outset;height:20px;color:white;''')
        self.del_bnt.setStyleSheet('''text-align:center;background-color: red;border-style:outset;height:20px;color:white;''')
        self.regret_bnt.setStyleSheet('''text-align:center;background-color: grey;border-style:outset;height:20px;color:white;''')
        self.print_bnt.setStyleSheet('''text-align:center;background-color: #660099;border-style:outset;height:20px;color:white;''')
        self.report_bnt.setStyleSheet('''text-align:center;background-color:#1c86ee;border-style:outset;height:20px;color:white;''')

        self.hlayout = QHBoxLayout()
        self.db.cur.execute('select serial_number,is_deleted,is_reported from death_info where serial_number = "%s"'%(self.query_id))
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        if rslt[-2] == 1:
            self.hlayout.addWidget(self.regret_bnt)
        elif rslt[-1] == 1:
            self.hlayout.addWidget(self.view_bnt)
            self.hlayout.addWidget(self.print_bnt)
            self.hlayout.addWidget(self.del_bnt)
        else:
            self.hlayout.addWidget(self.report_bnt)
            self.hlayout.addWidget(self.view_bnt)
            self.hlayout.addWidget(self.print_bnt)
            self.hlayout.addWidget(self.del_bnt)

        self.view_bnt.clicked.connect(lambda:self.view_record(rslt[0]))
        self.del_bnt.clicked.connect(lambda:self.del_record(rslt[0]))
        self.regret_bnt.clicked.connect(lambda:self.regret_record(rslt[0]))
        self.print_bnt.clicked.connect(lambda:self.print_record(rslt[0]))
        self.report_bnt.clicked.connect(lambda:self.report_record(rslt[0]))
        self.hlayout.setContentsMargins(5,2,5,2)
        self.widget.setLayout(self.hlayout)
        return self.widget

    def view_record(self,id):
        self.db = DataBase()
        self.db.cur.execute('select * from death_info where serial_number = %s'%(id))
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.a = regist.Regist(self.user)
        self.a.save_bnt.setText("更新")
        self.a.title.setText("查        看")

        self.report_distinct_code = str(rslt[1])
        report_distinct_name = address_dic.county_dic[self.report_distinct_code[:4]][self.report_distinct_code[:6]]
        self.a.report_distinct.setText(report_distinct_name)

        self.a.report_department.setCurrentIndex(int(rslt[45]))
        self.a.serial_number.setText(rslt[3])
        self.a.serial_number.setReadOnly(True)
        self.a.bianhao.setText(rslt[4])
        self.a.bianhao.setReadOnly(False)
        self.a.name.setText(rslt[5])
        self.a.gender_code.setText(str(rslt[6]))
        if rslt[6] == 1:
            self.a.male.setChecked(True)
        elif rslt[6] == 2:
            self.a.female.setChecked(True)
        elif rlst[6] == 3:
            self.a.unkonwn_gender.setChecked(True)
        else:
            self.a.unscript_gender.setChecked(True)

        self.a.race.setCurrentIndex(int(rslt[7]))
        self.a.id_class.setCurrentIndex(int(rslt[8]))
        self.a.id.setText(rslt[9])
        birthday_list = self.to_pydate(rslt[10])
        self.a.birthday.setDate(QDate(birthday_list[0],birthday_list[1],birthday_list[2]))
        death_date_list = self.to_pydate(rslt[21])
        self.a.death_date.setDate(QDate(death_date_list[0],death_date_list[1],death_date_list[2]))
        self.a.age.setText(rslt[11][:-1])
        self.a.age_unit.setCurrentText(rslt[11][-1])
        self.a.marriage.setCurrentIndex(int(rslt[12]))
        self.a.education.setCurrentIndex(int(rslt[13]))
        self.a.occupation.setCurrentIndex(int(rslt[14]))
        self.a.address_now.setText(rslt[15])
        self.a.code_now.setText(str(rslt[16]))
        self.a.address_birth.setText(rslt[17])
        self.a.code_birth.setText(str(rslt[18]))
        self.a.death_location.setCurrentIndex(int(rslt[19]))
        self.a.company.setText(rslt[20])
        self.a.family.setText(rslt[22])
        self.a.family_tel.setText(rslt[23])
        self.a.family_address.setText(rslt[24])
        self.a.disease_a.setText(rslt[25])
        self.a.disease_a_time.setText(str(rslt[26]))
        self.a.disease_a_time_unit.setCurrentText(rslt[27])
        self.a.disease_b.setText(rslt[28])
        self.a.disease_b_time.setText(str(rslt[29]))
        self.a.disease_b_time_unit.setCurrentText(rslt[30])
        self.a.disease_c.setText(rslt[31])
        self.a.disease_c_time.setText(str(rslt[32]))
        self.a.disease_c_time_unit.setCurrentText(rslt[33])
        self.a.disease_d.setText(rslt[34])
        self.a.disease_d_time.setText(str(rslt[35]))
        self.a.disease_d_time_unit.setCurrentText(rslt[36])
        self.a.other_disease.setText(rslt[37])
        self.a.death_reason.setText(rslt[38])
        self.a.diagnost_department.setCurrentIndex(int(rslt[39]))
        self.a.diagnost_method.setCurrentIndex(int(rslt[40]))
        self.a.inhospital.setText(rslt[41])
        self.a.doctor.setText(rslt[42])
        regist_list = self.to_pydate(rslt[43])
        self.a.regist_date.setDate(QDate(regist_list[0],regist_list[1],regist_list[2]))
        self.a.reporter.setText(rslt[44])
        self.a.reporter.setReadOnly(True)
        self.a.backup.setText(rslt[46])
        self.a.research.setText(rslt[47])
        self.a.researcher.setText(rslt[48])
        self.a.relation.setText(rslt[49])
        self.a.researcher_address.setText(rslt[50])
        self.a.researcher_tel.setText(rslt[51])
        self.a.death_reason2.setText(rslt[52])
        research_date_list = self.to_pydate(rslt[53])
        self.a.research_date.setDate(QDate(research_date_list[0],research_date_list[1],research_date_list[2]))

        self.a.back_bnt.setText('关闭(ESC)')
        self.a.back_bnt.clicked.disconnect(self.a.back_click)
        self.a.back_bnt.clicked.connect(self.a.close)
        self.a.save_bnt.setText('更新(ENT)')
        self.a.save_bnt.clicked.disconnect(self.a.save_record)
        self.a.save_bnt.clicked.connect(self.a.update_record)
        self.a.show()

    def del_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update death_info set is_deleted = 1 where serial_number = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_record()

    def regret_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update death_info set is_deleted = 0 where serial_number = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_record()

    def print_record(self, id):
        self.window = PrintWindow(id)
        self.window.show()

    def report_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update death_info set is_reported = 1 where serial_number = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_record()

    def clear_click(self):
        self.name.setText("")
        self.begin_date.setDate(QDate(2000,1,1))
        self.end_date.setDate(QDate.currentDate())

    def export_record(self):
        pass

    def close_window(self):
        self.close()
        self.listwindow = login.ListWindow(self.user)
        self.listwindow.show()

    def to_next_page(self):
        self.present_page += 1
        if self.present_page < self.max_page:
            a =  (self.present_page-1) * 20
        else:
            a = (self.max_page-1)*20
            self.present_page = self.max_page
        self.query_record(start=a)

    def to_pre_page(self):
        self.present_page -= 1
        if self.present_page == 0:
            self.present_page = 1
        else:
            self.present_page = self.present_page
        a = (self.present_page-1)*20
        self.query_record(start=a)

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

    def change_date(self,pyqtdate):   # a pyqtdate style /yyyymmdd to time stamp
        pydate = pyqtdate.date().toPyDate()
        base_date = datetime.date(1970,1,1)
        day_delta = pydate - base_date
        days = day_delta.days
        seconds = days*24*3600
        return seconds

    def to_date(self,a):
        b = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        c = b.strftime('%Y-%m-%d')
        return c

    def to_pydate(self,a):
        b = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return [b.year, b.month, b.day]

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            self.query_record()
