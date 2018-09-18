#!/usr/bin/env python
# coding:utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import hashlib
from data import *
import sys
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

        self.hospital= QLineEdit()
        self.hospital.setReadOnly(True)
        self.hospital.setStyleSheet('background-color:#f0f0f0;')

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
        self.close()
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
        self.username.setText(rslt_list[0])
        self.username.setReadOnly(True)
        self.name.setText(rslt_list[1])
        self.hospital.setText(str(rslt_list[7]))
        self.code.setText(str(rslt_list[8]))
        self.hospital_code.setText(rslt_list[9])
        self.reporter.setText(rslt_list[11])
        self.username.setStyleSheet('background-color:#f0f0f0;')

        if rslt_list[4] < 9:
            self.hospital_manage_bnt.setVisible(False)
        elif rslt_list[4] < 1:
            self.user_manage_bnt.setVisible(False)
        else:
            pass

    def confirm_click(self):

        self.db = DataBase()
        h5 = hashlib.md5()
        h5.update(self.password.text().encode(encoding='utf-8'))

        if self.confirm_bnt.text() == "确定(ENT)":
                if self.password.text() == '':
                    sql = 'update user set  nickname="%s" where username = "%s"'%(self.name.text(), self.user)
                elif self.password.text() == self.password2.text():
                    sql = 'update user set password = "%s", nickname="%s" where username = "%s"'%(h5.hexdigest(), self.name.text(), self.user)
                else:
                    self.message.setText('两次输入密码不一致')
                self.db.cur.execute(sql)
                msg = QMessageBox.information(self,'提示','确认修改',QMessageBox.Yes, QMessageBox.Yes)
                if msg == QMessageBox.Yes:
                    self.db.con.commit()
                else:
                    pass
        else:
            self.db.cur.execute("select id from hospital where name  = '%s'"%(self.hospital.text()))
            hospital_id = int(self.db.cur.fetchone()[0])
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
                        values ("{0}","{1}","{2}",{3},{4},{5})'''.format(self.username.text(), self.name.text(),h5.hexdigest(),hospital_id,0,0)
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
        self.setWindowTitle("用户列表")
        self.resize(800, 600)
        self.set_ui()

    def set_ui(self):
        self.db = DataBase()
        sql1 = '''select hospital_id, account_level from user where  username = "%s"'''%(self.user)
        self.db.cur.execute(sql1)
        rslt = self.db.cur.fetchone()
        if rslt[1] == 9:
            sql2 = '''select a.*, b.* from user as a, hospital as b where a.hospital_id = b.id'''
        else:
            id_rslt = rslt[0]
            sql2 = '''select a.*, b.* from user as a, hospital as b where a.hospital_id = b.id and
                 a.hospital_id = "%s"'''%(id_rslt)
        self.db.cur.execute(sql2)
        rslt2 = self.db.cur.fetchall()
        self.db.con.close()
        amount = len(rslt2)
        self.table = QTableWidget(amount, 6)
        self.table.verticalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(['帐号','姓名','医院','地区编码','医院组织机构单位','操作'])
        # self.table.resizeColumnToContents(5)
        self.table.setColumnWidth(5,120)
        k = 0
        x = [0,1,7,8,9]
        for i in rslt2:
            for j in range(5):
                y = str(i[x[j]])
                self.table.setItem(k,j,QTableWidgetItem(y))
            self.table.setCellWidget(k,5,self.button_row(i[0]))
            self.table.setRowHeight(k,40)
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
        self.view_bnt.setStyleSheet('''background-color:green; border-style:outset;color:white;''')
        self.del_bnt.setStyleSheet('background-color:red; border-style:outset;color:white;')
        self.regret_bnt.setStyleSheet('background-color:grey; border-style: outset;color:white;')

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


if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Login()
        # mainwindow = User_Info()
        mainwindow.show()
        sys.exit(app.exec_())
