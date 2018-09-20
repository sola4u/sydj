#!/usr/bin/env python
# coding:utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import hashlib
import sys
import datetime
from data import *
from regist import *


class Login(QWidget):

    def __init__(self):
        super(Login,self).__init__()
        self.setFixedSize(600,400)
        self.setWindowTitle("登录")
        self.set_ui()

    def set_ui(self):

        self.username = QLineEdit()
        self.username.setPlaceholderText("请输入用户名")
        self.username.setClearButtonEnabled(True)
        self.username.setFixedHeight(30)

        self.password = QLineEdit()
        self.password.setPlaceholderText("请输入密码")
        self.password.setClearButtonEnabled(True)
        self.password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setFixedHeight(30)
        self.password.setFont(QFont())

        self.bnt = QPushButton("登录")
        self.bnt.clicked.connect(self.signin)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.bnt)
        self.setLayout(self.layout)

    def signin(self):
        self.db = DataBase()
        username = self.username.text()
        password = self.password.text()
        if (username == '' or password == ''):
            QMessageBox.warning(self,'提示','用户名或密码为空', QMessageBox.Yes, QMessageBox.Yes)
            return
        sql = 'select * from user where username = "%s"'%username
        self.db.cur.execute(sql)
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        password_md5 = hashlib.md5()
        password_md5.update(password.encode(encoding='utf-8'))
        if not rslt:
            QMessageBox.information(self,'提示','帐号不存在',QMessageBox.Yes, QMessageBox.Yes)
        else:
            if password_md5.hexdigest() == rslt[2]:
                mainwindow.close()
                self.listwindow = ListWindow(username)
                self.listwindow.show()
            else:
                QMessageBox.information(self,'提示','用户名密码错误',QMessageBox.Yes, QMessageBox.Yes)
        return

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.signin()

class ListWindow(QWidget):

    def __init__(self, username):
        super(ListWindow,self).__init__()
        self.user = username
        self.setFixedSize(600, 400)
        self.setWindowTitle("登记")
        self.set_ui()

    def set_ui(self):
        self.regist = QPushButton("regist")
        self.query = QPushButton("query")
        self.user_info = QPushButton("user_info")
        self.regist.clicked.connect(self.regist_window)
        self.query.clicked.connect(self.query_window)
        self.user_info.clicked.connect(self.user_info_window)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.regist)
        self.layout.addWidget(self.query)
        self.layout.addWidget(self.user_info)
        self.setLayout(self.layout)

    def regist_window(self):
        self.close()
        self.window = Regist(self.user)
        self.window.show()

    def query_window(self):
        pass

    def user_info_window(self):
        self.close()
        self.window = User_Info(self.user)
        self.window.show()

class User(QWidget):

    def __init__(self):
        super(User, self).__init__()
        self.setWindowTitle('账号信息')
        self.setFixedSize(300, 400)
        self.set_ui()

    def set_ui(self):

        self.username = QLineEdit()
        self.name = QLineEdit()
        self.password= QLineEdit()
        self.password.setPlaceholderText('请输入密码')
        self.password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)

        self.password2= QLineEdit()
        self.password2.setPlaceholderText('请再次输入密码')
        self.password2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)


        self.hospital = QComboBox()
        self.db = DataBase()
        sql2 = 'select * from hospital'
        rslt2 = self.db.cur.execute(sql2)
        rslt2_list = self.db.cur.fetchall()
        self.db.con.close()
        for i in rslt2_list:
            self.hospital.addItem(i[1])
        self.hospital.setStyleSheet('background-color:#f0f0f0;')
        self.hospital.currentTextChanged.connect(self.hospital_info_autuofill)

        self.code = QLineEdit()
        self.code.setReadOnly(True)
        self.code.setStyleSheet('background-color:#f0f0f0;')
        self.hospital_code = QLineEdit()
        self.hospital_code.setReadOnly(True)
        self.hospital_code.setStyleSheet('background-color:#f0f0f0;')
        self.reporter = QLineEdit()
        self.reporter.setReadOnly(True)
        self.reporter.setStyleSheet('background-color:#f0f0f0;')

        self.user_manage_bnt = QPushButton("用户管理")
        self.user_manage_bnt.clicked.connect(self.user_manage)
        self.hospital_manage_bnt= QPushButton("医院管理")
        self.hospital_manage_bnt.clicked.connect(self.hospital_manage)
        self.confirm_bnt = QPushButton('确定(ENT)')
        self.confirm_bnt.clicked.connect(self.confirm_click)
        self.cancel_bnt = QPushButton('取消(ESC)')
        self.cancel_bnt.clicked.connect(self.back_click)

        self.message = QLabel()
        self.message.setStyleSheet('QLabel{color:red;font-size:20px;}')
        self.message.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.fbox = QFormLayout()
        self.toolbox = QHBoxLayout()

        self.fbox.addRow('用  户  名',self.username)
        self.fbox.addRow('姓      名',self.name)
        self.fbox.addRow('密      码',self.password)
        self.fbox.addRow('确 认 密 码',self.password2)
        self.fbox.addRow('单 位 名 称',self.hospital)
        self.fbox.addRow('地 区 编 码', self.code)
        self.fbox.addRow('医院机构代码', self.hospital_code)
        self.fbox.addRow('报  告  人', self.reporter)

        self.toolbox.addWidget(self.hospital_manage_bnt)
        self.toolbox.addWidget(self.user_manage_bnt)
        self.toolbox.addWidget(self.confirm_bnt)
        self.toolbox.addWidget(self.cancel_bnt)

        self.f2box = QWidget()
        self.tool2box = QWidget()

        self.f2box.setLayout(self.fbox)
        self.tool2box.setLayout(self.toolbox)

        self.vbox.addWidget(self.f2box)
        self.vbox.addWidget(self.message)
        self.vbox.addWidget(self.tool2box)

        self.setLayout(self.vbox)

    def confirm_click(self):
        pass

    def hospital_manage(self):
        # self.close()
        self.list_window = Hospital_List()
        self.list_window.show()

    def back_click(self):
        self.close()
        self.a = ListWindow(self.user)
        self.a.show()

    def user_manage(self):
        self.close()
        self.a = User_List(self.user)
        self.a.show()

    def hospital_info_autuofill(self):
        self.db = DataBase()
        name = self.hospital.currentText()
        sql = 'select * from hospital where name = "%s"'%(name)
        tmp = self.db.cur.execute(sql)
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.code.setText(rslt[3])
        self.reporter.setText(rslt[5])


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()
        if e.key() == Qt.Key_Return:
            self.confirm_click()

class User_Info(User):

    def __init__(self,user):
        super(User_Info,self).__init__()
        self.setFixedSize(600, 400)
        self.db = DataBase()
        self.user = user
        sql = '''select a.*, b.* from user as a, hospital as b
                where username  = "%s" and a.hospital_id = b.id'''%self.user
        rslt = self.db.cur.execute(sql)
        rslt_list = rslt.fetchone()
        self.hospital_id = rslt_list[3]
        self.db.con.close()
        self.username.setText(rslt_list[0])
        self.username.setReadOnly(True)
        self.name.setText(rslt_list[1])
        self.code.setText(str(rslt_list[8]))
        self.hospital_code.setText(rslt_list[9])
        self.hospital.setCurrentText(rslt_list[7])
        self.reporter.setText(rslt_list[11])
        self.username.setStyleSheet('background-color:#f0f0f0;')

        if rslt_list[4] < 9:
            self.hospital_manage_bnt.setVisible(False)
        if rslt_list[4] < 1:
            self.user_manage_bnt.setVisible(False)
        if rslt_list[4] == 9:
            self.code.setReadOnly(False)
            self.reporter.setReadOnly(False)


    def confirm_click(self):

        self.db = DataBase()
        h5 = hashlib.md5()
        h5.update(self.password.text().encode(encoding='utf-8'))
        # self.db.cur.execute("select account_level from user where username = '%s'"%(self.user))
        # accout_level = self.db.cur.fetchone()[0]

        if self.confirm_bnt.text() == "确定(ENT)":
                # if self.accout_level < 9:
                    # if self.password.text() == '':
                        # sql = 'update user set  nickname="%s" where username = "%s"'%(self.name.text(), self.user)
                    # elif self.password.text() == self.password2.text():
                        # sql = 'update user set password = "%s", nickname="%s" where username = "%s"'%(h5.hexdigest(), self.name.text(), self.user)
                    # else:
                        # self.message.setText('两次输入密码不一致')
                # else:
                if self.password.text() == '':
                    sql = 'update user set  nickname="%s",hospital_id = "%s" where username = "%s"'%(self.name.text(),self.hospital_id, self.user)
                elif self.password.text() == self.password2.text():
                    sql = 'update user set password = "%s", nickname="%s",hospital_id = "%s" where username = "%s"'%(h5.hexdigest(), self.name.text(), self.hospital_id,self.user)
                else:
                    self.message.setText('两次输入密码不一致')
                self.db.cur.execute(sql)
                print(sql)
                msg = QMessageBox.information(self,'提示','确认修改',QMessageBox.Yes, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    self.db.con.commit()
                else:
                    pass
        else:
            if self.password.text() == '':
                self.message.setText("密码未填写")
            elif self.password.text() != self.password2.text():
                self.message.setText('两次输入密码不一致')
            else:
                self.db.cur.execute('select * from user where username = "%s"'%(self.username.text()))
                if self.db.cur.fetchall():
                    self.message.setText("用户已经存在")
                else:
                    sql = '''insert into user (username, nickname,password,hospital_id,account_level,is_delete)
                        values ("{0}","{1}","{2}",{3},{4},{5})'''.format(self.username.text(), self.name.text(),h5.hexdigest(),hospital_id,self.account_level,0)
                    self.db.cur.execute(sql)
                    msg = QMessageBox.information(self,'提示','确认修改',QMessageBox.Yes, QMessageBox.Yes)
                    if msg == QMessageBox.Yes:
                        self.db.con.commit()
                    else:
                        pass
        self.db.con.close()


class User_List(QWidget):

    def __init__(self, user):
        super(User_List, self).__init__()
        self.user = user
        self.db = DataBase()
        sql1 = '''select hospital_id, account_level from user where  username = "%s"'''%(self.user)
        self.db.cur.execute(sql1)
        self.rslt = self.db.cur.fetchone()
        if self.rslt[1] == 9:
            sql2 = '''select a.*, b.* from user as a, hospital as b where a.hospital_id = b.id'''
        else:
            id_rslt = self.rslt[0]
            sql2 = '''select a.*, b.* from user as a, hospital as b where a.hospital_id = b.id and
                 a.hospital_id = "%s"'''%(id_rslt)
        self.db.cur.execute(sql2)
        self.rslt2 = self.db.cur.fetchall()
        self.db.con.close()
        self.setWindowTitle("用户列表")
        self.resize(800, 600)
        self.set_ui()

    def set_ui(self):
        amount = len(self.rslt2)
        self.table = QTableWidget(amount, 6)
        self.table.verticalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(['帐号','姓名','医院','地区编码','医院组织机构单位','操作'])
        # self.table.resizeColumnToContents(5)
        self.table.setColumnWidth(5,120)
        k = 0
        x = [0,1,7,8,9]
        for i in self.rslt2:
            for j in range(5):
                y = str(i[x[j]])
                self.table.setItem(k,j,QTableWidgetItem(y))
            self.table.setCellWidget(k,5,self.button_row(i[0]))
            self.table.setRowHeight(k,40)
            self.table.setColumnWidth(k,120)
            k += 1
        self.db.con.close()

        self.add_bnt = QPushButton('add_user')
        self.add_bnt.clicked.connect(self.add_user)
        self.close_bnt = QPushButton("close")
        self.close_bnt.clicked.connect(self.close_click)
        self.bnt_layout = QHBoxLayout()
        self.bnt_layout.addWidget(self.add_bnt)
        self.bnt_layout.addWidget(self.close_bnt)
        self.bnt_layout2 = QWidget()
        self.bnt_layout2.setLayout(self.bnt_layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.bnt_layout2)
        self.setLayout(self.layout)

    def button_row(self,username):
        self.view_bnt = QPushButton("查看")
        self.del_bnt = QPushButton("停用")
        self.regret_bnt = QPushButton('重新启用')
        self.view_bnt.setStyleSheet('''background-color:green; height:60px; border-style:outset;color:white;''')
        self.del_bnt.setStyleSheet('background-color:red; height:60px; border-style:outset;color:white;')
        self.regret_bnt.setStyleSheet('background-color:grey; height:60px; border-style: outset;color:white;')

        self.view_bnt.clicked.connect(lambda:self.view_record(username))
        self.del_bnt.clicked.connect(lambda:self.del_record(username))
        self.regret_bnt.clicked.connect(lambda:self.regret_record(username))

        self.layout = QHBoxLayout()
        self.widget = QWidget()

        self.db = DataBase()
        self.db.cur.execute("select is_delete from user where username = '%s'"%(username))
        rslt = self.db.cur.fetchone()[0]
        self.db.con.close()
        if rslt:
            self.layout.addWidget(self.regret_bnt)
        else:
            self.layout.addWidget(self.view_bnt)
            self.layout.addWidget(self.del_bnt)
        self.widget.setLayout(self.layout)
        return self.widget

    def add_user(self):
        self.a = User_Info(self.user)
        self.a.show()
        self.a.username.setText('')
        self.a.username.setReadOnly(False)
        self.a.name.setText('')
        self.a.user_manage_bnt.setVisible(False)
        self.a.cancel_bnt.clicked.disconnect(self.a.back_click)
        self.a.cancel_bnt.clicked.connect(lambda:self.a.close())
        self.a.username.setStyleSheet('background-color:white;')
        self.a.confirm_bnt.setText("添加")


    def del_record(self, username):
        self.db = DataBase()
        self.db.cur.execute('update user set is_delete = 1 where username = "%s"'%(username))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.close()
        self.a = User_List(self.user)
        self.a.show()

    def view_record(self, username):
        self.a = User_Info(username)
        self.a.show()
        self.a.username.setReadOnly(False)
        self.a.user_manage_bnt.setVisible(False)
        self.a.cancel_bnt.clicked.disconnect(self.a.back_click)
        if self.rslt[1] < 9:
            self.a.hospital.currentTextChanged.disconnect(self.a.hospital_info_autuofill)
        # self.a.cancel_bnt.clicked.connect(lambda:self.a.close())
        self.a.cancel_bnt.clicked.connect(self.view_close_click)

    def regret_record(self, username):
        self.db = DataBase()
        self.db.cur.execute('update user set is_delete = 0 where username = "%s"'%(username))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.close()
        self.a = User_List(self.user)
        self.a.show()

    def close_click(self):
        self.close()
        self.a = ListWindow(self.user)
        self.a.show()

    def view_close_click(self):
        self.close()
        self.a = User_List(self.user)
        self.a.show()

class Hospital_List(QWidget):

    def __init__(self):
        super(Hospital_List, self).__init__()
        self.setFixedSize(600, 400)

        self.add_bnt = QPushButton("添加")
        self.back_bnt = QPushButton("close")
        self.add_bnt.clicked.connect(self.add_record)
        self.back_bnt.clicked.connect(self.back_click)

        self.db = DataBase()
        self.db.cur.execute("select id,name,code,depart_code,reporter from hospital")
        rslt = self.db.cur.fetchall()
        self.db.con.close()
        column = len(rslt)
        self.table = QTableWidget(column, 6)
        self.table.setHorizontalHeaderLabels(['医院编码','医院名称','地区代码','组织机构代码','报告人','操作'])
        k = 0
        for i in rslt:
            for j in range(len(i)):
                x = str(i[j])
                self.table.setItem(k,j,QTableWidgetItem(x))
                self.table.setColumnWidth(k,80)
                self.table.setRowHeight(k,40)
            self.table.setCellWidget(k,5,self.button_row(i[0]))
            k += 1


        self.layout = QVBoxLayout()
        self.bnt_layout = QHBoxLayout()
        self.bnt_layout2 = QWidget()

        self.bnt_layout.addWidget(self.add_bnt)
        self.bnt_layout.addWidget(self.back_bnt)

        self.bnt_layout2.setLayout(self.bnt_layout)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.bnt_layout2)
        self.setLayout(self.layout)

    def button_row(self, id):
        self.edit_bnt = QPushButton("查看")
        self.del_bnt = QPushButton("停用")
        self.regret_bnt = QPushButton("重新启用")
        self.edit_bnt.setStyleSheet('''background-color:green; border-style:outset;height:60px; color:white;''')
        self.del_bnt.setStyleSheet('''background-color:red; border-style:outset; height:60px; color:white;''')
        self.regret_bnt.setStyleSheet('''background-color:blue; border-style:outset; height:60px; color:white;''')
        self.edit_bnt.clicked.connect(lambda:self.edit_record(id))
        self.del_bnt.clicked.connect(lambda:self.del_record(id))
        self.regret_bnt.clicked.connect(lambda:self.regret_record(id))

        self.layout = QHBoxLayout()
        self.widget = QWidget()
        self.db = DataBase()
        self.db.cur.execute("select is_delete from hospital where id = %d"%(id))
        rslt = self.db.cur.fetchone()[0]
        self.db.con.close()
        if rslt:
            self.layout.addWidget(self.regret_bnt)
        else:
            self.layout.addWidget(self.edit_bnt)
            self.layout.addWidget(self.del_bnt)
        self.widget.setLayout(self.layout)
        return self.widget


    def add_record(self):
        self.close()
        self.a = Hospital_Info(0)
        self.a.show()
        self.a.confirm_bnt.setText("添加")

    def edit_record(self, id):
        self.close()
        self.a = Hospital_Info(id)
        self.a.show()
        self.a.confirm_bnt.setText("更新")
        self.a.id.setReadOnly(True)

    def del_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update hospital set is_delete = 1 where id = %d'%(id))
        self.db.con.commit()
        self.db.con.close()
        self.close()
        self.a = Hospital_List()
        self.a.show()

    def regret_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update hospital set is_delete = 0 where id = %d'%(id))
        self.db.con.commit()
        self.db.con.close()
        self.close()
        self.a = Hospital_List()
        self.a.show()

    def back_click(self):
        self.close()

class Hospital_Info(QWidget):

    def __init__(self, id):
        super(Hospital_Info, self).__init__()
        self.setFixedSize(400, 600)
        self.setWindowTitle("医院信息")
        self.hospital_id = id
        self.set_ui()

    def set_ui(self):
        self.id_lable = QLabel("编号")
        self.id = QLineEdit()
        self.name_label = QLabel("医院名称")
        self.name = QLineEdit()
        self.code_lael = QLabel("地区编码")
        self.code = QLineEdit()
        self.depart_code_label = QLabel("组织机构代码")
        self.depart_code = QLineEdit()
        self.reporter_label = QLabel("报告人")
        self.reporter = QLineEdit()
        self.confirm_bnt = QPushButton("确定")
        self.close_bnt= QPushButton("取消")
        self.confirm_bnt.clicked.connect(self.confirm_click)
        self.close_bnt.clicked.connect(self.close_click)

        if self.hospital_id:
            self.db = DataBase()
            self.db.cur.execute("select * from hospital where id = %d"%(self.hospital_id))
            rslt = self.db.cur.fetchone()
            self.db.con.close()
            self.id.setText(str(rslt[0]))
            self.name.setText(rslt[1])
            self.code.setText(str(rslt[2]))
            self.depart_code.setText(rslt[3])
            self.reporter.setText(rslt[5])

        self.layout = QGridLayout()
        self.layout.addWidget(self.id_lable,0,0)
        self.layout.addWidget(self.id,0,1)
        self.layout.addWidget(self.name_label,1,0)
        self.layout.addWidget(self.name,1,1)
        self.layout.addWidget(self.code_lael,2,0)
        self.layout.addWidget(self.code,2,1)
        self.layout.addWidget(self.depart_code_label,3,0)
        self.layout.addWidget(self.depart_code,3,1)
        self.layout.addWidget(self.reporter_label,4,0)
        self.layout.addWidget(self.reporter,4,1)

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout.addWidget(self.confirm_bnt)
        self.bnt_layout.addWidget(self.close_bnt)
        self.bnt_layout2 = QWidget()
        self.bnt_layout2.setLayout(self.bnt_layout)
        self.grid_layout = QWidget()
        self.grid_layout.setLayout(self.layout)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.grid_layout)
        self.main_layout.addWidget(self.bnt_layout2)
        self.setLayout(self.main_layout)

    def confirm_click(self):
        self.close()
        self.db = DataBase()
        if self.confirm_bnt.text() == "添加":
            self.db.cur.execute("select id from hospital where id = %d"%(int(self.id.text())))
            rslt = self.db.cur.fetchone()
            if rslt:
                QMessageBox.warning(self,'tips','用户已存在',QMessageBox.Yes,QMessageBox.Yes)
            else:
                sql1 = 'insert into hospital values ({0},"{1}",{2},"{3}",{4},"{5}")'.format(int(self.id.text()), self.name.text(),int(self.code.text()),self.depart_code.text(),0,self.reporter.text())
                sql2 = 'insert into bianhao values ({0},{1},{2},{3})'.format(int(self.id.text()),'1',datetime.datetime.now().year,1)
                self.db.cur.execute(sql1)
                self.db.cur.execute(sql2)
                msg = QMessageBox.information(self, "tips",'确认提交',QMessageBox.Yes, QMessageBox.No)
                if msg == QMessageBox.Yes:
                    self.db.con.commit()
                else:
                    pass
        else:
            sql = '''update hospital set id = %d,name = "%s",code = %d,
                        depart_code="%s",reporter="%s" where id = %d'''%(int(self.id.text()), self.name.text(),int(self.code.text()),self.depart_code.text(),self.reporter.text(),self.hospital_id)
            self.db.cur.execute(sql)
            msg = QMessageBox.information(self, "tips",'确认提交',QMessageBox.Yes, QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.db.con.commit()
            else:
                pass
        self.db.con.close()
        self.a = Hospital_List()
        self.a.show()

    def close_click(self):
        self.close()


if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Login()
        mainwindow.show()
        sys.exit(app.exec_())
