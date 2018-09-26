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
        # self.db.cur.execute("select hospital_id from user where username = '%s'"%(self.user))
        # hospital_id = self.db.cur.fetchone()[0]
        # # # # self.db.cur.execute("select count(*) from death_info where hospital_code = '%s'"%(hospital_id))
        # # # rslt = self.db.cur.fetchone()
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
        self.end_date_bnt = QPushButton()
        self.end_date_bnt.setStyleSheet("border:hidden;")
        self.end_date_bnt.setIcon(QIcon('cal2.png'))
        self.end_date_bnt.clicked.connect(self.end_date_choose)
        self.department_label = QLabel("单    位")
        self.department = QComboBox()
        for i in hospital_list:
            self.department.addItem(i)
        self.all_record = QRadioButton("所有记录")
        self.all_record.setChecked(True)
        self.unreport_report = QRadioButton("未上报")
        self.undelete_report = QRadioButton("所有记录(含删除)")
        self.by_report_date = QRadioButton("按报告日期")
        self.by_report_date.setChecked(True)
        self.by_death_date = QRadioButton("按死亡日期")

        self.query_bnt = QPushButton("查询")
        self.requery_bnt = QPushButton("重置")
        self.export_bnt = QPushButton("导出Excel")
        self.close_bnt = QPushButton("关闭")
        self.query_bnt.clicked.connect(lambda:self.query_record())
        self.requery_bnt.clicked.connect(self.requery)
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

        self.choose_record_layout = QHBoxLayout()
        self.choose_date_layout = QHBoxLayout()
        self.choose_record_layout.addWidget(self.all_record)
        self.choose_record_layout.addWidget(self.unreport_report)
        self.choose_record_layout.addWidget(self.undelete_report)
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

    def query_click(self,start = 0, numbers = 20):
        self.db = DataBase()
        self.numbers =  numbers
        self.start = start
        if self.name.text() == '':
            name_sql = ' and name like "%"'
        else:
            name_text = '%' + self.name.text() + '%'
            name_sql = ' and name like "%s"'%(name_text)

        if self.all_record.isChecked():
            is_deleted_sql = ''
        else:
            is_deleted_sql = 'and is_deleted = 0 '
        if self.death_date.isChecked():
            date_sql = 'deathdate'
        else:
            date_sql = 'regist_date'
        a = RegistWindow()
        begin_date_interge = a.change_date(self.begin_date)
        end_date_interge = a.change_date(self.end_date)
        sql = '''
            select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where date2 between %d and %d
            '''%(begin_date_interge,end_date_interge)
        number_sql = 'select count(*) from base where date2 between %d and %d '%(begin_date_interge,end_date_interge)
        if self.id.text() != "":
            sql2 = 'select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where id = %s limit %d offset %d'%(self.id.text(),self.numbers, self.start)
            sql3 = 'select count(*) from base where id = %s '%(self.id.text())
        else:
            sql2 = sql.replace('date2',date_sql) + is_deleted_sql + name_sql + '  limit %d offset %d'%(self.numbers,self.start)
            sql3 = number_sql.replace('date2',date_sql) + is_deleted_sql + name_sql
        rlst_exec = self.db.cur.execute(sql2)
        rslt =  rlst_exec.fetchall()
        count = self.db.cur.execute(sql3).fetchone()[0]
        pages = ceil(count/self.numbers)
        pages_text = '共' + str(count) +'条 ' + str(pages) + '页，第' + str(self.this_page) +'页'
        self.page.setText(pages_text)
        self.max_page = pages
        k = 0
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['编号','姓名','身份证号码','性别','出生日期','常住地址','死亡日期','死亡原因','登记日期','是否报告','操作'])
        for i in rslt:
            for j in range(9):
                if j in [4,6,8]:
                    self.table.setItem(k,j,QTableWidgetItem(self.to_date(i[j])))
                else:
                    self.table.setItem(k,j,QTableWidgetItem(i[j]))
            self.table.setCellWidget(k,10,self.button_row(i[0]))
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

        self.view_bnt.setStyleSheet('''text-align:center; background-color:green;border-style:outset;height:20px;color:white;''')
        self.del_bnt.setStyleSheet('''text-align:center;background-color: red;border-style:outset;height:20px;color:white;''')
        self.regret_bnt.setStyleSheet('''text-align:center;background-color: grey;border-style:outset;height:20px;color:white;''')
        self.print_bnt.setStyleSheet('''text-align:center;background-color: #660099;border-style:outset;height:20px;color:white;''')

        self.hlayout = QHBoxLayout()
        self.db.cur.execute('select * from death_info where serialnumber = %s'%(self.query_id))
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        if rslt[-1] == 1:
            self.hlayout.addWidget(self.regret_bnt)
        else:
            self.hlayout.addWidget(self.view_bnt)
            self.hlayout.addWidget(self.print_bnt)
            self.hlayout.addWidget(self.del_bnt)
        self.view_bnt.clicked.connect(lambda:self.view_record(rslt[3]))
        self.del_bnt.clicked.connect(lambda:self.del_record(rslt[3]))
        self.regret_bnt.clicked.connect(lambda:self.regret_record(rslt[3]))
        self.print_bnt.clicked.connect(lambda:self.print_record(rslt[3]))
        self.hlayout.setContentsMargins(5,2,5,2)
        self.widget.setLayout(self.hlayout)
        return self.widget

    def view_record(self,id):
        self.db = DataBase()
        self.db.cur.execute('select * from base where serialnumber = %s'%(id))
        b = self.db.cur.fetchone()
        self.db.con.close()
        self.a = RegistWindow()
        self.a.serialnumber.setText(b[0])
        self.a.serialnumber.setReadOnly(True)
        self.a.name.setText(b[1])
        self.a.id.setText(b[2])
        self.a.gender.setText(b[3])
        if b[3] == '男':
            self.a.male.setChecked(True)
        else:
            self.a.female.setChecked(True)
        self.a.race.setToolTip(b[4])
        birthday_list = self.to_pydate(b[5])
        self.a.birthday.setDate(QDate(birthday_list[0],birthday_list[1],birthday_list[2]))
        self.a.address.setText(b[6])
        deathdate_list = self.to_pydate(b[7])
        self.a.deathdate.setDate(QDate(deathdate_list[0],deathdate_list[1],deathdate_list[2]))
        self.a.disease.setText(b[8])
        self.a.family.setText(b[9])
        self.a.tel.setText(b[10])
        regist_list = self.to_pydate(b[11])
        self.a.regist_date.setDate(QDate(regist_list[0],regist_list[1],regist_list[2]))
        self.a.serialnumber2 = b[0]
        self.a.blank.setText("==========查  看==========")
        self.a.back_bnt.setText('关闭(ESC)')
        self.a.back_bnt.clicked.disconnect(self.a.back_click)
        self.a.back_bnt.clicked.connect(self.a.close)
        self.a.save_bnt.clicked.disconnect(self.a.save_record)
        self.a.save_bnt.clicked.connect(self.a.update_record)
        self.a.save_bnt.setText('更新(F2)')
        self.a.show()

    def del_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update base set is_deleted = 1 where serialnumber = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_click()

    def regret_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update base set is_deleted = 0 where serialnumber = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_click()

    def print_record(self, id):
        self.window = PrintWindow(id)
        self.window.show()


    def close_window(self):
        self.close()

    def to_pre_page(self):
        pass

    def to_next_page(self):
        pass


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
