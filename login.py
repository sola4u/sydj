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
        sql = 'select * from user where id = "%s"'%username
        self.db.cur.execute(sql)
        rslt = self.db.cur.fetchone()
        md5 = hashlib.md5()
        # password_md5 = md5.update(password.encode(encoding='utf-8')).hexdigest()
        password_md5 = password
        if not rslt:
            QMessageBox.information(self,'提示','帐号不存在',QMessageBox.Yes, QMessageBox.Yes)
        else:
            if password_md5 == rslt[2]:
                self.db.con.close()
                mainwindow.close()
                self.listwindow = ListWindow(username)
                self.listwindow.show()
            else:
                QMessageBox.information(self,'提示','用户名密码错误',QMessageBox.Yes, QMessageBox.Yes)
        return

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
        self.window = User(self.user)
        self.window.show()

class User(QWidget):

    def __init__(self,user):
        super(User,self).__init__()
        self.setWindowTitle('账号信息')
        self.user = user
        self.setFixedSize(300, 400)
        self.set_ui()

    def set_ui(self):
        self.db = DataBase()
        rslt = self.db.cur.execute('select * from user where id = "%s"'%self.user)
        rslt_list = rslt.fetchone()
        self.db.con.close()

        self.username = QLineEdit()
        self.username.setText(User_List[0])
        self.username.setReadOnly(True)
        self.username.setStyleSheet('background-color:#f0f0f0;')

        self.name = QLineEdit()
        self.name.setText(rslt_list[1])
        self.name.setReadOnly(True)
        self.name.setStyleSheet('background-color:#f0f0f0;')

        self.password= QLineEdit()
        self.password.setPlaceholderText('请输入密码')
        self.password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)

        self.password2= QLineEdit()
        self.password2.setPlaceholderText('请再次输入密码')
        self.password2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)

        self.hospital= QLineEdit()
        self.hospital.setText(infolist[3])
        self.hospital.setPlaceholderText('请输入单位名称')
        self.hospital.setClearButtonEnabled(True)

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

        self.fbox.addRow('姓名',self.name)
        self.fbox.addRow('密码',self.password)
        self.fbox.addRow('确认密码',self.password2)
        self.fbox.addRow('单位名称',self.hospital)

        self.toolbox.addWidget(self.cancel_bnt)
        self.toolbox.addWidget(self.confirm_bnt)

        self.f2box = QWidget()
        self.tool2box = QWidget()

        self.f2box.setLayout(self.fbox)
        self.tool2box.setLayout(self.toolbox)

        self.vbox.addWidget(self.f2box)
        self.vbox.addWidget(self.message)
        self.vbox.addWidget(self.tool2box)

        self.setLayout(self.vbox)

    def confirm_click(self):
        if self.password.text() == self.password2.text():
            a = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
            if a == QMessageBox.Yes:
                h5 = hashlib.md5()
                h5.update(self.password.text().encode(encoding='utf-8'))
                query = self.cur
                if self.password.text() == '':
                    query.execute('update user set  department="%s"'%(self.department.text()))
                else:
                    query.execute('update user set password = "%s", department="%s"'%(h5.hexdigest(), self.department.text()))
                self.con.commit()
                self.message.setText(self.password.text())
                self.close()
                self.a = ListWindow()
                self.a.show()
            else:
                pass
        else:
            self.message.setText('两次输入密码不一致')


    def back_click(self):
        self.db.con.close()
        self.close()
        self.a = ListWindow()
        self.a.show()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()
        if e.key() == Qt.Key_Return:
            self.confirm_click()

class User_List(QWidget):

    def __init__(self):
        super(User_List, self).__init__()
        self.setWindowTitle("用户列表")
        self.set_ui()

    def set_ui(self):
        pass

    def add_user(self):
        pass

    def del_user(self):
        pass

if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainwindow = Login()
        mainwindow.show()
        sys.exit(app.exec_())
