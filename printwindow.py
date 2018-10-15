
#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5 import QtWidgets
from data import *
import address_dic
import datetime
import print_modle
import sys


class PrintWindow(QWidget):

    def __init__(self,id):
        super(PrintWindow, self).__init__()
        self.text = str(id)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(Qt.black)
        qp.setFont(QFont('宋体', 16,QFont.Bold))
        qp.drawText(0,0,800,50, Qt.AlignCenter, "居民死亡医学证明（推断）书")
        qp.setFont(QFont('宋体', 9))
        qp.drawText(90,40,800,20, Qt.AlignLeft, "安徽省黄山市黄山区")
        qp.drawText(90,60,400,20, Qt.AlignLeft, "行政区划代码 34100300")
        qp.drawText(400,60,310,20, Qt.AlignLeft, "编号：123456789100")
        qp.drawRect(80,80,80,36)
        qp.drawText(85,85,80,30, Qt.AlignCenter, "死者姓名")
        qp.drawRect(160,80,144,36)
        qp.drawRect(304,80,50,36)
        qp.drawText(304,85,50,30,Qt.AlignCenter,'性别')
        qp.drawRect(354,80,124,36)
        qp.drawRect(478,80,56,36)
        qp.drawText(478,85,56,30,Qt.AlignCenter,'民族')
        qp.drawRect(534,80,84,36)
        qp.drawRect(618,80,66,36)
        qp.drawText(618,85,66,15,Qt.AlignCenter,'国家或')
        qp.drawText(618,85,66,45,Qt.AlignCenter,'地区')
        qp.drawRect(684,80,84,36)






class PrintWindow2(QWidget):

    def __init__(self,id):
        super(PrintWindow2, self).__init__()
        self.id = id
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        # self.setFixedSize(800,600)
        self.resize(1200,800)
        self.setWindowTitle("打印")
        self.set_ui()

    def set_ui(self):
        self.db = DataBase()
        self.db.cur.execute("select * from death_info where  serial_number = '%s'"%(self.id))
        self.rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.list_dic = Choice_Dic()
        for i in range(len(self.rslt)):
            print(i, self.rslt[i])
        if self.rslt:
            province = address_dic.province_dic[self.rslt[1][:2]]
            city = address_dic.city_dic[self.rslt[1][:2]][self.rslt[1][:4]]
            county = address_dic.county_dic[self.rslt[1][:4]][self.rslt[1][:6]]
            address = province + city + county
            gender = self.list_dic.gender_list[self.rslt[6]]
            race = self.list_dic.race_list[self.rslt[7]]
            id_class = self.list_dic.id_class_list[self.rslt[8]]
            marriage = self.list_dic.marriage_list[self.rslt[12]]
            education = self.list_dic.education_list[self.rslt[13]]
            occupation = self.list_dic.occupation_list[self.rslt[14]]
            death_location = self.list_dic.death_location_list[self.rslt[19]]
            diagnost_department = self.list_dic.diagnost_department_list[self.rslt[39]]
            diagnost_method = self.list_dic.diagnost_method_list[self.rslt[40]]
            a = print_modle.html_page1
            html_page2 = a.format(address,self.rslt[1],self.rslt[4],self.rslt[5],gender,race,id_class,self.rslt[9],
                        self.rslt[11],marriage,self.change_date(self.rslt[10]),education,occupation,
                        self.change_date(self.rslt[21]),death_location,'否',self.rslt[20],self.rslt[17],
                        self.rslt[15],self.rslt[22], self.rslt[23],self.rslt[24],self.rslt[25],str(self.rslt[26])+self.rslt[27],
                        self.rslt[28],str(self.rslt[29])+self.rslt[30], self.rslt[31], str(self.rslt[32])+self.rslt[33],
                        self.rslt[34], str(self.rslt[35])+self.rslt[36],self.rslt[37],diagnost_department,diagnost_method,
                        self.change_date(self.rslt[53]),self.rslt[38],0,0,0,0,0,0,0,0)
            html_page1 = print_modle.test_page
        else:
            text = '''<h1>无此条记录</h1>
            '''
        print(html_page1)
        self.close_bnt = QPushButton("关闭")
        self.close_bnt.clicked.connect(self.close_click)
        self.print_bnt1 = QPushButton("打印第二联")
        self.print_bnt2 = QPushButton('打印')
        self.print_bnt2.clicked.connect(lambda:self.print_page1(html_page1))
        self.print_bnt3 = QPushButton('无模版打印')

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout.addWidget(self.print_bnt1)
        self.bnt_layout.addWidget(self.print_bnt2)
        self.bnt_layout.addWidget(self.close_bnt)

        self.bnt_layout2 = QWidget()
        self.bnt_layout2.setLayout(self.bnt_layout)

        self.content = QTextEdit()
        self.content.insertHtml(html_page1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bnt_layout2)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)

    def close_click(self):
        self.close()

    def print_page1(self, htmltxt):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(htmltxt)
            document.print_(self.printer)
        self.close()

    def print_page1_4a4(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(html_page1_4a4)
            document.print_(self.printer)
        self.close()

    def print_page2(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(html_page1_4a4)
            document.print_(self.printer)
        self.close()

    def print_page2_4a4(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(html_page1_4a4)
            document.print_(self.printer)
        self.close()

    def to_page2(self):
        pass

    def to_page1(self):
        pass

    def change_date(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month) +'月'+str(date.day)+'日'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = PrintWindow(0)
    mainwindow.show()
    sys.exit(app.exec_())
