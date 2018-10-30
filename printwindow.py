#!/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog
from PyQt5 import QtWidgets
from data import *
import address_dic
import datetime
import sys,os
import platform


plat_form = platform.platform()
if 'Windows' in plat_form:
    import win32print
    import win32api
else:
    pass


class PrintWindow(QWidget):

    def __init__(self, id, label):
        super(PrintWindow, self).__init__()
        self.setFixedSize(810, 700)
        self.setWindowTitle("打印")
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.id = str(id)
        self.label = label
        self.db = DataBase()
        self.db.cur.execute('select name from death_info where serial_number = "%s"'%(self.id))
        self.name = self.db.cur.fetchone()[0]
        self.db.con.close()
        self.set_ui()

    def  set_ui(self):
        self.layout = QVBoxLayout()

        self.print_bnt = QPushButton("打印(ENT)")
        self.print_data_bnt = QPushButton("仅打印数据")
        self.change_page_bnt= QPushButton("查看第二联")
        self.save_bnt = QPushButton("保存(F5)")
        self.close_bnt = QPushButton('关闭(ESC)')
        self.print_bnt.clicked.connect(self.print_page)
        self.print_data_bnt.clicked.connect(self.print_page1_data)
        self.close_bnt.clicked.connect(self.close_page)
        self.change_page_bnt.clicked.connect(self.change_page)
        self.save_bnt.clicked.connect(self.save_page)

        self.pic = PaintArea(self.id, self.label)

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout.addStretch(4)
        self.bnt_layout.addWidget(self.print_bnt)
        self.bnt_layout.addWidget(self.print_data_bnt)
        self.bnt_layout.addWidget(self.change_page_bnt)
        if self.label%2 == 1:
            self.bnt_layout.addWidget(self.save_bnt)
        self.bnt_layout.addWidget(self.close_bnt)

        self.bnt_layout2 = QWidget()
        self.bnt_layout2.setLayout(self.bnt_layout)

        self.layout.addWidget(self.pic)
        # self.layout.addWidget(self.a)

        self.scroll = QScrollArea(self)
        self.scroll.setAutoFillBackground(True)
        self.scroll.setMinimumSize(800, 600)
        self.scroll.setWidgetResizable(True)
        self.scroll_bar = self.scroll.verticalScrollBar()

        self.layout2 = QWidget()
        self.layout2.setLayout(self.layout)

        self.scroll.setWidget(self.layout2)

        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.bnt_layout2)
        self.layout3.addWidget(self.scroll)
        self.layout3.addStretch()

        self.setLayout(self.layout3)

    def print_page(self):
        plat_form = platform.platform()
        if 'Windows' in plat_form:
            self.printer = Print_Setting()
            self.printer.show()
            self.printer.printer_signal.connect(self.print_confirm)
        else:
            pass
        self.close()

    def print_confirm(self, str):
        # currentprinter = win32print.GetDefaultPrinter()
        currentprinter = str
        win32api.ShellExecute(0,'print','tmp.pdf','/d:%s'%currentprinter,'.',0)
        self.close()

    def close_page(self):
        self.close()

    def print_page1_data(self):
        self.new_window = PrintWindow(self.id,2)
        self.new_window.show()
        self.new_window.change_page_bnt.setText("查看第一联")
        self.new_window.print_data_bnt.setText("打印第二联数据")
        self.new_window.print_data_bnt.clicked.disconnect(self.new_window.print_page1_data)
        self.new_window.print_data_bnt.clicked.connect(self.new_window.print_page2_data)
        # self.new_window.save_bnt.clicked.disconnect(self.new_window.save_page1)
        # self.new_window.save_bnt.clicked.connect(self.new_window.save_page2)
        self.close()

    def save_page(self):
        filename,ok = QFileDialog.getSaveFileName(self,'savefile','%s.pdf'%(self.name+self.id))
        fileinfo = QFileInfo(filename)
        if fileinfo.exists():
            QFile.remove(filename)
        QFile.copy('tmp.pdf', filename)

    def print_page2_data(self):
        self.new_window = PrintWindow(self.id,4)
        self.new_window.show()
        self.new_window.change_page_bnt.setText("查看第二联")
        self.new_window.print_data_bnt.setText("打印第一联数据")
        # self.new_window.print_data_bnt.clicked.connect(self.new_window.print_page1_data)
        self.close()

    def change_page(self):
        if self.change_page_bnt.text() == '查看第二联':
            self.new_window = PrintWindow(self.id,3)
            self.new_window.show()
            self.new_window.change_page_bnt.setText("查看第一联")
            self.new_window.print_data_bnt.setText("打印第二联数据")
            self.new_window.print_data_bnt.clicked.disconnect(self.new_window.print_page1_data)
            self.new_window.print_data_bnt.clicked.connect(self.new_window.print_page2_data)
            self.close()
        else:
            self.new_window = PrintWindow(self.id,1)
            self.new_window.show()
            self.new_window.change_page_bnt.setText("查看第二联")
            self.new_window.print_data_bnt.setText("打印第一联数据")
            # self.new_window.print_data_bnt.clicked.connect(self.new_window.print_page1_data)
            self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.print_page()
        elif e.key() == Qt.Key_Escape:
            self.close_page()
        elif e.key() == Qt.F5:
            self.save_page()


class PaintArea(QWidget):

    def __init__(self,id,label):
        super(PaintArea, self).__init__()
        self.id= str(id)
        self.label = label
        self.setFixedSize(760, 1080)
        self.printer = QPrinter()
        self.db = DataBase()
        self.db.cur.execute("select * from death_info where  serial_number = '%s'"%(self.id))
        self.rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.list_dic = Choice_Dic()
        if self.rslt:
            province = address_dic.province_dic[self.rslt[1][:2]]
            city = address_dic.city_dic[self.rslt[1][:2]][self.rslt[1][:4]]
            county = address_dic.county_dic[self.rslt[1][:4]][self.rslt[1][:6]]
            address = [province,city,county]
            gender = self.list_dic.gender_list[self.rslt[6]]
            race = self.list_dic.race_list[self.rslt[7]]
            id_class = self.list_dic.id_class_list[self.rslt[9]]
            marriage = self.list_dic.marriage_list[self.rslt[13]]
            education = self.list_dic.education_list[self.rslt[14]]
            occupation = self.list_dic.occupation_list[self.rslt[15]]
            death_location = self.list_dic.death_location_list[self.rslt[20]]
            diagnost_department = self.list_dic.diagnost_department_list[self.rslt[41]]
            diagnost_method = self.list_dic.diagnost_method_list[self.rslt[42]]
            self.rslt_list = [address,self.rslt[1],self.rslt[4],self.rslt[5],gender,race,id_class,self.rslt[10],
                        self.rslt[12],marriage,self.change_date(self.rslt[11]),education,occupation,
                        self.change_datetime(self.rslt[22]),death_location,'否',self.rslt[21],self.rslt[18],
                        self.rslt[16],self.rslt[23], self.rslt[24],self.rslt[25],self.rslt[26],str(self.rslt[27])+self.rslt[28],
                        self.rslt[29],str(self.rslt[30])+self.rslt[31], self.rslt[32], str(self.rslt[33])+self.rslt[34],
                        self.rslt[35], str(self.rslt[36])+self.rslt[37],self.rslt[38],diagnost_department,diagnost_method,
                        self.change_date(self.rslt[45]),self.rslt[39],self.rslt[40],self.rslt[49],self.rslt[50],self.rslt[51],
                        self.rslt[53],self.rslt[52],self.rslt[54],self.change_date(self.rslt[55]),self.rslt[8],self.rslt[12]]

    def paintEvent(self, event):
        qp = QPainter(self)
        if self.label == 1:
            self.draw_page1(event, qp)
        elif self.label == 2:
            self.draw_page1_data(event, qp)
        elif self.label == 3:
            self.draw_page2(event, qp)
        else:
            self.draw_page2_data(event, qp)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setOutputFileName('./tmp.pdf')
        qp = QPainter(self.printer)
        if self.label == 1:
            self.draw_page1(event, qp)
        elif self.label == 2:
            self.draw_page1_data(event, qp)
        elif self.label == 3:
            self.draw_page2(event, qp)
        else:
            self.draw_page2_data(event, qp)

    def draw_page1(self,event, qp):
        qp.setPen(QPen(Qt.black,1))
        qp.setFont(QFont('宋体', 16,QFont.Bold))
        qp.drawText(0,60,800,50, Qt.AlignCenter, "居民死亡医学证明（推断）书")
        qp.setFont(QFont('宋体', 9))
        distinct = ' '.join(self.rslt_list[0])
        qp.drawText(50,110,800,14.2, Qt.AlignLeft, distinct)
        qp.setFont(QFont('Arial', 10))
        qp.drawText(50,128,400,23.9, Qt.AlignLeft, "行政区划代码 %s"%(self.rslt_list[1]))
        qp.drawText(450,128,300,23.9, Qt.AlignLeft, "编号：%s"%(self.rslt_list[2]))
        qp.setFont(QFont('宋体', 9))

        x = 150
        qp.drawRect(30,x,80,36)
        qp.drawRect(110,x,144,36)
        qp.drawRect(254,x,50,36)
        qp.drawRect(304,x,124,36)
        qp.drawRect(428,x,55,36)
        qp.drawRect(483,x,82,36)
        qp.drawRect(565,x,60,36)
        qp.drawRect(625,x,120,36)
        qp.drawText(30,x,80,30, Qt.AlignCenter,'死者姓名')
        qp.drawText(110,x,144,30, Qt.AlignCenter,self.rslt_list[3])
        qp.drawText(254,x,50,30,Qt.AlignCenter,'性别')
        qp.drawText(304,x,124,30,Qt.AlignCenter,self.rslt_list[4])
        qp.drawText(428,x,55,30,Qt.AlignCenter,'民族')
        qp.drawText(483,x,82,30,Qt.AlignCenter,self.rslt_list[5])
        qp.drawText(565,x,60,20,Qt.AlignCenter,'国家或')
        qp.drawText(565,x,60,50,Qt.AlignCenter,'地区')
        qp.drawText(625,x,120,30,Qt.AlignCenter,self.rslt_list[-2])

        x += 36
        qp.drawRect(30,x,80, 68)
        qp.drawRect(110,x,144,68)
        qp.drawRect(254,x,50,68)
        qp.drawRect(304,x,124,68)
        qp.drawRect(428,x,55,68)
        qp.drawRect(483,x,82,68)
        qp.drawRect(565,x,60,68)
        qp.drawRect(625,x,120,68)
        qp.drawText(30,x,80,40,Qt.AlignCenter,'有效身份')
        qp.drawText(30,x,80,80,Qt.AlignCenter,'证件类别')
        qp.drawText(110,x,144,65, Qt.AlignCenter,self.rslt_list[6])
        qp.drawText(254,x,50,40,Qt.AlignCenter,'证件')
        qp.drawText(254,x,50,80,Qt.AlignCenter,'号码')
        qp.drawText(304,x,124,65,Qt.AlignCenter,self.rslt_list[7])
        qp.drawText(428,x,55,65,Qt.AlignCenter,'年龄')
        qp.drawText(483,x,82,65,Qt.AlignCenter,self.rslt_list[8])
        qp.drawText(565,x,60,40,Qt.AlignCenter,'婚姻')
        qp.drawText(565,x,60,80,Qt.AlignCenter,'状况')
        qp.drawText(625,x,120,65,Qt.AlignCenter,self.rslt_list[9])

        x += 68
        qp.drawRect(30,x,80,68)
        qp.drawRect(110,x,144,68)
        qp.drawRect(254,x,50,68)
        qp.drawRect(304,x,124,68)
        qp.drawRect(428,x,55,68)
        qp.drawRect(483,x,262,68)
        qp.drawText(30,x+5,80,35,Qt.AlignCenter,'出生')
        qp.drawText(30,x+5,80,65,Qt.AlignCenter,'日期')
        qp.drawText(110,x,144,65, Qt.AlignCenter,self.rslt_list[10])
        qp.drawText(254,x,50,40,Qt.AlignCenter,'文化')
        qp.drawText(254,x,50,80,Qt.AlignCenter,'程度')
        qp.drawText(304,x,124,65,Qt.AlignCenter,self.rslt_list[11])
        qp.drawText(428,x,55,40,Qt.AlignCenter,'个人')
        qp.drawText(428,x,55,80,Qt.AlignCenter,'身份')
        qp.drawText(483,x,262,65,Qt.AlignCenter,self.rslt_list[12])

        x += 68
        qp.drawRect(30,x,80,36)
        qp.drawRect(110,x,144,36)
        qp.drawRect(254,x,50,36)
        qp.drawRect(304,x,179,36)
        qp.drawRect(483,x,142,36)
        qp.drawRect(625,x,120,36)
        qp.drawText(30,x,80,30,Qt.AlignCenter,'死亡日期')
        date_time = self.rslt_list[13].split('/')
        qp.drawText(115,x+5,110,30,Qt.AlignRight|Qt.AlignTop,date_time[0])
        qp.drawText(115,x,110,30,Qt.AlignRight|Qt.AlignBottom,date_time[1])
        qp.drawText(254,x,50,20,Qt.AlignCenter,'死亡')
        qp.drawText(254,x,50,50,Qt.AlignCenter,'地点')
        qp.drawText(304,x,179,30,Qt.AlignCenter,self.rslt_list[14])
        qp.drawText(483,x,142,20,Qt.AlignCenter,'死亡时是否处于妊娠期')
        qp.drawText(483,x,142,50,Qt.AlignCenter,'或妊娠终止后42天内')
        qp.drawText(625,x,120,30,Qt.AlignCenter,self.rslt_list[15])

        x += 36
        qp.drawRect(30,x,80,36)
        qp.drawRect(110,x,144,36)
        qp.drawRect(254,x,50,36)
        qp.drawRect(304,x,179,36)
        qp.drawRect(483,x,82,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,80,20,Qt.AlignCenter,'生前')
        qp.drawText(30,x,80,50,Qt.AlignCenter,'工作单位')
        qp.drawText(110,x,144,30,Qt.AlignCenter,self.rslt_list[16])
        qp.drawText(254,x,50,20,Qt.AlignCenter,'户籍')
        qp.drawText(254,x,50,50,Qt.AlignCenter,'地址')
        address_a_length = len(self.rslt_list[17])
        if address_a_length < 14:
            qp.drawText(310, x, 179, 30, Qt.AlignCenter,self.rslt_list[17])
        else:
            for i in range(address_a_length%14):
                qp.drawText(310,x + 5 + 15*i,179,25,Qt.AlignTop|Qt.AlignLeft,self.rslt_list[17][14*i:14*(i+1)])
        qp.drawText(483,x,82,20,Qt.AlignCenter,'常住')
        qp.drawText(483,x,82,50,Qt.AlignCenter,'地址')
        address_b_length = len(self.rslt_list[18])
        if address_b_length < 1:
            qp.drawText(570, x, 180, 30, Qt.AlignCenter,self.rslt_list[18])
        else:
            for i in range(address_b_length%13):
                qp.drawText(570,x + 5 + 15*i,180,25,Qt.AlignLeft|Qt.AlignTop,self.rslt_list[18][13*i:13*(i+1)])

        x += 36
        qp.drawRect(30,x,80,36)
        qp.drawRect(110,x,144,36)
        qp.drawRect(254,x,50,36)
        qp.drawRect(304,x,179,36)
        qp.drawRect(483,x,82,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,80,20,Qt.AlignCenter,'可联系的')
        qp.drawText(30,x,80,50,Qt.AlignCenter,'家属姓名')
        qp.drawText(110,x,144,30,Qt.AlignCenter,self.rslt_list[19])
        qp.drawText(254,x,50,20,Qt.AlignCenter,'联系')
        qp.drawText(254,x,50,50,Qt.AlignCenter,'电话')
        qp.drawText(304,x,179,30,Qt.AlignCenter,self.rslt_list[20])
        qp.drawText(483,x,82,20,Qt.AlignCenter,'家属住址')
        qp.drawText(483,x,82,50,Qt.AlignCenter,'或工作单位')
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[21])

        x += 36
        qp.drawRect(30,x,224,36)
        qp.drawRect(254,x,311,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,224,30,Qt.AlignCenter,'致死的主要疾病诊断')
        qp.drawText(254,x,311,30,Qt.AlignCenter,'疾病名称(勿填症状体征)')
        qp.drawText(565,x,180,30,Qt.AlignCenter,'发病至死亡大概间隔时间')

        x += 36
        qp.drawRect(30,x,224,36)
        qp.drawRect(254,x,311,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,224,30,Qt.AlignCenter,'Ⅰ.(a)直接死亡原因')
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[22])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[23])


        x += 36
        qp.drawRect(30,x,224,36)
        qp.drawRect(254,x,311,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,224,30,Qt.AlignCenter,'(b)引起(a)的疾病或情况')
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[24])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[25])

        x += 36
        qp.drawRect(30,x,224,36)
        qp.drawRect(254,x,311,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,224,30,Qt.AlignCenter,'(c)引起(b)的疾病或情况')
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[26])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[27])

        x += 36
        qp.drawRect(30,x,224,36)
        qp.drawRect(254,x,311,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,224,30,Qt.AlignCenter,'(d)引起(c)的疾病或情况')
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[28])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[29])

        x += 36
        qp.drawRect(30,x,224,40)
        qp.drawRect(254,x,311,40)
        qp.drawRect(565,x,180,40)
        qp.drawText(40,x,219,25,Qt.AlignCenter,'Ⅱ.其他疾病诊断(促进死亡，但与')
        qp.drawText(40,x,219,55,Qt.AlignCenter,'导致死亡无关的其他重要情况)')
        qp.drawText(259,x,319,36,Qt.AlignCenter,self.rslt_list[30])
        qp.drawText(578,x,150,36,Qt.AlignCenter,'')

        x += 40
        qp.drawRect(30,x,80,40)
        qp.drawRect(110,x,373,40)
        qp.drawRect(483,x,82,40)
        qp.drawRect(565,x,180,40)
        qp.drawText(30,x,80,25,Qt.AlignCenter,'生前主要疾病')
        qp.drawText(30,x,80,55,Qt.AlignCenter,'最高诊断单位')
        qp.drawText(110,x,373,36,Qt.AlignCenter,self.rslt_list[31])
        qp.drawText(483,x,82,25,Qt.AlignCenter,'生前主要疾病')
        qp.drawText(483,x,82,55,Qt.AlignCenter,'最高诊断依据')
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[32])

        x += 40
        qp.drawRect(30,x,80,40)
        qp.drawRect(110,x,144,40)
        qp.drawRect(254,x,50,40)
        qp.drawRect(304,x,179,40)
        qp.drawRect(483,x,82,40)
        qp.drawRect(565,x,180,40)
        qp.drawText(30,x,80,36,Qt.AlignCenter,'医师签名')
        qp.drawText(254,x,50,25,Qt.AlignCenter,'医疗卫生')
        qp.drawText(254,x,50,55,Qt.AlignCenter,'机构盖章')
        qp.drawText(483,x,82,36,Qt.AlignCenter,'填表日期')
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[33])

        x += 40
        qp.drawRect(30,x,224,40)
        qp.drawRect(254,x,229,40)
        qp.drawRect(483,x,82,40)
        qp.drawRect(565,x,180,40)
        qp.drawText(30,x,224,36,Qt.AlignCenter,'(以下由编码人员填写)根本死亡原因:')
        qp.drawText(254,x,229,36,Qt.AlignCenter,self.rslt_list[34])
        qp.drawText(483,x,82,36,Qt.AlignCenter,'ICD编码:')
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[35])

        x += 40
        qp.setFont(QFont('宋体', 14,QFont.Bold))
        qp.drawText(40,x,688,30,Qt.AlignCenter,'死亡调查记录')
        qp.setFont(QFont('宋体', 9))

        x += 32
        qp.drawRect(30,x,715,128)
        qp.drawText(30,x,150,36,Qt.AlignCenter,'死者生前病史及症状体征:')
        research_len = len(self.rslt_list[36])
        for i in range(research_len%55):
            qp.drawText(50,x+30*(1+i),700,36,Qt.AlignLeft,self.rslt_list[36][i*55:(i+1)*55])
        qp.drawText(438,x+110,250,36,Qt.AlignLeft,'以上情况属实，被调查者签字:')

        x += 128
        qp.drawRect(30,x,80,36)
        qp.drawRect(110,x,100,36)
        qp.drawRect(210,x,44,36)
        qp.drawRect(254,x,50,36)
        qp.drawRect(304,x,80,36)
        qp.drawRect(384,x,99,36)
        qp.drawRect(483,x,82,36)
        qp.drawRect(565,x,180,36)
        qp.drawText(30,x,80,20,Qt.AlignCenter,'被调查者')
        qp.drawText(30,x,80,50,Qt.AlignCenter,'姓名')
        qp.drawText(110,x,100,30,Qt.AlignCenter,self.rslt_list[37])
        qp.drawText(210,x,44,20,Qt.AlignCenter,'与死者')
        qp.drawText(210,x,44,50,Qt.AlignCenter,'关系')
        qp.drawText(254,x,50,30,Qt.AlignCenter,self.rslt_list[38])
        qp.drawText(304,x,80,20,Qt.AlignCenter,'联系')
        qp.drawText(304,x,80,50,Qt.AlignCenter,'电话')
        qp.drawText(384,x,99,30,Qt.AlignCenter,self.rslt_list[39])
        qp.drawText(483,x,82,20,Qt.AlignCenter,'联系地址')
        qp.drawText(483,x,82,50,Qt.AlignCenter,'或工作单位')
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[40])

        x += 36
        qp.drawRect(30,x,80,20)
        qp.drawRect(110,x,194,20)
        qp.drawRect(304,x,80,20)
        qp.drawRect(384,x,99,20)
        qp.drawRect(483,x,82,20)
        qp.drawRect(565,x,180,20)
        qp.drawText(30,x,80,18,Qt.AlignCenter,'死因推断')
        qp.drawText(110,x,194,18,Qt.AlignCenter,self.rslt_list[41])
        qp.drawText(304,x,80,18,Qt.AlignCenter,'被调查者签名')
        qp.drawText(483,x,82,18,Qt.AlignCenter,'调查日期')
        qp.drawText(565,x,180,18,Qt.AlignCenter,self.rslt_list[42])

        x += 30
        qp.drawText(40,x,688,18,Qt.AlignLeft,'注：①此表填写范围为在家、养老服务机构、其他场所正常死亡镇；②被调查者应为死者近亲或知情人；③调查时应出具以下资料:')

        x += 20
        qp.drawText(40,x,688,18,Qt.AlignLeft,'被调查者有效身份证件，居住地居委会或村委会证明，死者身份证和/或户口簿、生前病史卡.')


    def draw_page1_data(self,event, qp):
        qp.setPen(QPen(Qt.black,1))
        qp.setFont(QFont('宋体', 9))

        qp.drawText(50,110,80,14.2, Qt.AlignLeft, self.rslt_list[0][0])
        qp.drawText(250,110,80,14.2, Qt.AlignLeft, self.rslt_list[0][1])
        qp.drawText(430,110,80,14.2, Qt.AlignLeft, self.rslt_list[0][2])
        qp.setFont(QFont('Arial', 10))
        qp.drawText(120,125,400,23.9, Qt.AlignLeft, "%s"%(self.rslt_list[1]))
        qp.drawText(430,125,300,23.9, Qt.AlignLeft, "%s"%(self.rslt_list[2]))
        qp.setFont(QFont("宋体", 9))

        x = 150
        qp.drawText(110,x,144,30, Qt.AlignCenter,self.rslt_list[3])
        qp.drawText(304,x,124,30,Qt.AlignCenter,self.rslt_list[4])
        qp.drawText(483,x,82,30,Qt.AlignCenter,self.rslt_list[5])
        qp.drawText(625,x,120,30,Qt.AlignCenter,self.rslt_list[-2])

        x += 36
        qp.drawText(110,x,144,65, Qt.AlignCenter,self.rslt_list[6])
        qp.drawText(304,x,124,65,Qt.AlignCenter,self.rslt_list[7])
        qp.drawText(483,x,82,65,Qt.AlignCenter,self.rslt_list[8])
        qp.drawText(625,x,120,65,Qt.AlignCenter,self.rslt_list[9])

        x += 68
        qp.drawText(110,x,144,65, Qt.AlignCenter,self.rslt_list[10])
        qp.drawText(304,x,124,65,Qt.AlignCenter,self.rslt_list[11])
        qp.drawText(483,x,262,65,Qt.AlignCenter,self.rslt_list[12])

        x += 68
        date_time = self.rslt_list[13].split('/')
        qp.drawText(115,x+5,110,30,Qt.AlignRight|Qt.AlignTop,date_time[0])
        qp.drawText(115,x,110,30,Qt.AlignRight|Qt.AlignBottom,date_time[1])
        qp.drawText(304,x,179,30,Qt.AlignCenter,self.rslt_list[14])
        qp.drawText(625,x,120,30,Qt.AlignCenter,self.rslt_list[15])

        x += 36
        qp.drawText(110,x,144,30,Qt.AlignCenter,self.rslt_list[16])
        address_a_length = len(self.rslt_list[17])
        for i in range(address_a_length%14):
            qp.drawText(310,x + 5 + 15*i,179,25,Qt.AlignTop|Qt.AlignLeft,self.rslt_list[17][14*i:14*(i+1)])
        address_b_length = len(self.rslt_list[18])
        for i in range(address_b_length%13):
            qp.drawText(570,x + 5 + 15*i,180,25,Qt.AlignLeft|Qt.AlignTop,self.rslt_list[18][13*i:13*(i+1)])

        x += 36
        qp.drawText(110,x,144,30,Qt.AlignCenter,self.rslt_list[19])
        qp.drawText(304,x,179,30,Qt.AlignCenter,self.rslt_list[20])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[21])

        x += 72
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[22])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[23])

        x += 36
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[24])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[25])

        x += 36
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[26])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[27])

        x += 36
        qp.drawText(254,x,311,30,Qt.AlignCenter,self.rslt_list[28])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[29])

        x += 36
        qp.drawText(259,x,319,36,Qt.AlignCenter,self.rslt_list[30])
        qp.drawText(578,x,150,36,Qt.AlignCenter,'')

        x += 40
        qp.drawText(110,x,373,36,Qt.AlignCenter,self.rslt_list[31])
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[32])

        x += 40
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[33])

        x += 40
        qp.drawText(254,x,229,36,Qt.AlignCenter,self.rslt_list[34])
        qp.drawText(565,x,180,36,Qt.AlignCenter,self.rslt_list[35])

        x += 72
        research_len = len(self.rslt_list[36])
        for i in range(research_len%55):
            qp.drawText(50,x+30*(1+i),700,36,Qt.AlignLeft,self.rslt_list[36][i*55:(i+1)*55])

        x += 128
        qp.drawText(110,x,100,30,Qt.AlignCenter,self.rslt_list[37])
        qp.drawText(254,x,50,30,Qt.AlignCenter,self.rslt_list[38])
        qp.drawText(384,x,99,30,Qt.AlignCenter,self.rslt_list[39])
        qp.drawText(565,x,180,30,Qt.AlignCenter,self.rslt_list[40])

        x += 36
        qp.drawText(110,x,194,18,Qt.AlignCenter,self.rslt_list[41])
        qp.drawText(565,x,180,18,Qt.AlignCenter,self.rslt_list[42])

    def draw_page2(self, event, qp):
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for i in range(3):
            qp.setFont(QFont('宋体', 14,QFont.Bold))
            if i == 0:
                qp.drawText(0,50 + i*330,740,50, Qt.AlignCenter, "居民死亡医学证明（推断）书")
                qp.setFont(QFont('宋体', 9))
                qp.rotate(90)
                qp.drawText(150, -60, 150,30, Qt.AlignCenter, "第二联 公安机关保存")
                qp.rotate(-90)
            elif i == 1:
                qp.drawText(0,50 + i*330,740,50, Qt.AlignCenter, "居民死亡医学证明（推断）书")
                qp.setFont(QFont('宋体', 9))
                qp.rotate(90)
                qp.drawText(150 + i*320, -60, 150,30, Qt.AlignCenter, "第三联 死者家属保存")
                qp.rotate(-90)
            else:
                qp.drawText(0,50 + i*330,740,50, Qt.AlignCenter, "居民死亡殡葬证")
                qp.setFont(QFont('宋体', 9))
                qp.rotate(90)
                qp.drawText(150 + i*320, -60, 150,30, Qt.AlignCenter, "第四联 殡葬管理部门保存")
                qp.rotate(-90)

            x = 100 + 320*i
            qp.setFont(QFont('Arial', 10))
            qp.drawText(80,x,400,20, Qt.AlignLeft, "行政区划代码 %s"%(self.rslt_list[1]))
            qp.drawText(500,x,300,20, Qt.AlignLeft, "编号：%s"%(self.rslt_list[2]))
            qp.setFont(QFont('宋体', 9))

            x += 20
            qp.drawRect(70, x, 60, 36)
            qp.drawRect(130, x, 100, 36)
            qp.drawRect(230, x, 60, 36)
            qp.drawRect(290, x, 60, 36)
            qp.drawRect(350, x, 60, 36)
            qp.drawRect(410, x, 60, 36)
            qp.drawRect(470, x, 60, 36)
            qp.drawRect(530, x, 60, 36)
            qp.drawRect(590, x, 60, 36)
            qp.drawRect(650, x, 60, 36)
            qp.drawText(70, x, 60, 20, Qt.AlignCenter,'死者')
            qp.drawText(70, x, 60, 50, Qt.AlignCenter,'姓名')
            qp.drawText(230, x, 60, 30, Qt.AlignCenter,'性别')
            qp.drawText(350, x, 60, 30, Qt.AlignCenter,'民族')
            qp.drawText(470, x, 60, 20, Qt.AlignCenter,'国家或')
            qp.drawText(470, x, 60, 50, Qt.AlignCenter,'地区')
            qp.drawText(590, x, 60, 30, Qt.AlignCenter,'年龄')
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[3])
            qp.drawText(290, x, 60, 30, Qt.AlignCenter,self.rslt_list[4])
            qp.drawText(410, x, 60, 30, Qt.AlignCenter,self.rslt_list[5])
            qp.drawText(530, x, 60, 30, Qt.AlignCenter,self.rslt_list[-2])
            qp.drawText(650, x, 60, 30, Qt.AlignCenter,self.rslt_list[-1])

            x += 36
            qp.drawRect(70, x, 60, 36)
            qp.drawRect(130, x, 100, 36)
            qp.drawRect(230, x, 60, 36)
            qp.drawRect(290, x, 120, 36)
            qp.drawRect(410, x, 60, 36)
            qp.drawRect(470, x, 240, 36)
            qp.drawText(70, x, 60, 20, Qt.AlignCenter,'身份证件')
            qp.drawText(70, x, 60, 50, Qt.AlignCenter,'类别')
            qp.drawText(230, x, 60, 20, Qt.AlignCenter,'证件')
            qp.drawText(230, x, 60, 50, Qt.AlignCenter,'号码')
            qp.drawText(410, x, 60, 20, Qt.AlignCenter,'常住')
            qp.drawText(410, x, 60, 50, Qt.AlignCenter,'地址')
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[6])
            qp.drawText(290, x, 120, 30, Qt.AlignCenter,self.rslt_list[7])
            # qp.drawText(470, x, 240, 30, Qt.AlignCenter,self.rslt_list[18])
            address_length = len(self.rslt_list[17])
            if address_length < 18:
                qp.drawText(480, x, 240, 30, Qt.AlignCenter,self.rslt_list[17])
            else:
                for i in range(address_length%18):
                    qp.drawText(480,x + 5 + 15*i,240,25,Qt.AlignLeft|Qt.AlignTop,self.rslt_list[17][18*i:18*(i+1)])

            x += 36
            qp.drawRect(70, x, 60, 36)
            qp.drawRect(130, x, 100, 36)
            qp.drawRect(230, x, 60, 36)
            qp.drawRect(290, x, 120, 36)
            qp.drawRect(410, x, 60, 36)
            qp.drawRect(470, x, 240, 36)
            qp.drawText(70, x, 60, 20, Qt.AlignCenter,'出生')
            qp.drawText(70, x, 60, 50, Qt.AlignCenter,'日期')
            qp.drawText(230, x, 60, 20, Qt.AlignCenter,'死亡')
            qp.drawText(230, x, 60, 50, Qt.AlignCenter,'日期')
            qp.drawText(410, x, 60, 20, Qt.AlignCenter,'死亡')
            qp.drawText(410, x, 60, 50, Qt.AlignCenter,'地点')
            death_date = self.rslt_list[13].split('/')[0]
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[10])
            qp.drawText(290, x, 120, 30, Qt.AlignCenter,death_date)
            qp.drawText(470, x, 240, 30, Qt.AlignCenter,self.rslt_list[14])

            x += 36
            qp.drawRect(70, x, 60, 36)
            qp.drawRect(130, x, 220, 36)
            qp.drawRect(350, x, 60, 36)
            qp.drawRect(410, x, 120, 36)
            qp.drawRect(530, x, 60, 36)
            qp.drawRect(590, x, 120, 36)
            qp.drawText(70, x, 60, 20, Qt.AlignCenter,'死亡')
            qp.drawText(70, x, 60, 50, Qt.AlignCenter,'原因')
            qp.drawText(350, x, 60, 20, Qt.AlignCenter,'家属')
            qp.drawText(350, x, 60, 50, Qt.AlignCenter,'姓名')
            qp.drawText(530, x, 60, 20, Qt.AlignCenter,'联系')
            qp.drawText(530, x, 60, 50, Qt.AlignCenter,'电话')
            death_reason_len = len(self.rslt_list[22])
            if death_reason_len < 16:
                qp.drawText(130, x, 220, 30, Qt.AlignCenter,self.rslt_list[22])
            else:
                for i in range(death_reason_len%16):
                    qp.drawText(140, x + 5 + 15*i, 220, 25, Qt.AlignLeft|Qt.AlignTop,self.rslt_list[22][i*16:(i+1)*16])

            qp.drawText(410, x, 120, 30, Qt.AlignCenter,self.rslt_list[19])
            qp.drawText(590, x, 120, 30, Qt.AlignCenter,self.rslt_list[20])

            x += 36
            qp.drawRect(70, x, 60, 36)
            qp.drawRect(130, x, 220, 36)
            qp.drawRect(350, x, 60, 36)
            qp.drawRect(410, x, 120, 36)
            qp.drawRect(530, x, 60, 36)
            qp.drawRect(590, x, 120, 36)
            qp.drawText(70, x, 60, 20, Qt.AlignCenter,'家属住址')
            qp.drawText(70, x, 60, 50, Qt.AlignCenter,'或单位')
            qp.drawText(350, x, 60, 20, Qt.AlignCenter,'医师')
            qp.drawText(350, x, 60, 50, Qt.AlignCenter,'签名')
            qp.drawText(530, x, 60, 20, Qt.AlignCenter,'民警')
            qp.drawText(530, x, 60, 50, Qt.AlignCenter,'签名')
            qp.drawText(130, x, 220, 30, Qt.AlignCenter,self.rslt_list[21])

            x += 36
            qp.drawRect(70, x, 340, 52)
            qp.drawRect(410, x, 300, 52)
            qp.drawText(80,x+5,120,30,Qt.AlignLeft,'医疗卫生机构盖章')
            qp.drawText(80,x+35,300,30,Qt.AlignRight,self.rslt_list[33])
            qp.drawText(420,x+5,300,30,Qt.AlignLeft,'派出所意见（盖章）')
            qp.drawText(420,x+35,280,30,Qt.AlignRight,'     年    月   日')

            x += 60
            qp.setFont(QFont('宋体', 8))
            if i == 0:
                text ='''注：①死者家属持此联到公安机关办理户籍注销手续；②无医师及民警签字、医疗卫生机构及派出所盖章无效。'''
            elif i == 1:
                text ='''注：①死者家属持此联到公安机关签章；②无医师及民警签字、医疗卫生机构及派出所盖章无效；③死于救治机构以外的死亡原因
系死后推断。 '''
            else:
                text ='''注：①死者家属持此证到殡仪馆办理尸体火化手续；②死于救治机构，医师签字以及医疗卫生机构盖章有效；死于非救治机构，
医师及民警签字、医疗卫生机构及派出所盖章有效。'''
            qp.drawText(70, x, 700,30, Qt.AlignLeft,text)

        qp.setPen(QPen(Qt.black, 1, Qt.DashLine))
        qp.drawLine(QPointF(40, 390), QPointF(730, 390))
        qp.drawLine(QPointF(40, 720), QPointF(730, 720))


    def draw_page2_data(self, event, qp):
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        for i in range(3):
            x = 100 + 320*i
            qp.setFont(QFont('Arial', 10))
            qp.drawText(180,x,400,20, Qt.AlignLeft, "%s"%(self.rslt_list[1]))
            qp.drawText(400,x,300,20, Qt.AlignLeft, "%s"%(self.rslt_list[2]))
            qp.setFont(QFont('宋体', 9))

            x += 20
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[3])
            qp.drawText(290, x, 60, 30, Qt.AlignCenter,self.rslt_list[4])
            qp.drawText(410, x, 60, 30, Qt.AlignCenter,self.rslt_list[5])
            qp.drawText(530, x, 60, 30, Qt.AlignCenter,self.rslt_list[-2])
            qp.drawText(650, x, 60, 30, Qt.AlignCenter,self.rslt_list[-1])

            x += 36
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[6])
            qp.drawText(290, x, 120, 30, Qt.AlignCenter,self.rslt_list[7])
            # qp.drawText(470, x, 240, 30, Qt.AlignCenter,self.rslt_list[18])
            address_length = len(self.rslt_list[17])
            if address_length < 18:
                qp.drawText(480, x, 240, 30, Qt.AlignCenter,self.rslt_list[17])
            else:
                for i in range(address_length%18):
                    qp.drawText(480,x + 5 + 15*i,240,25,Qt.AlignLeft|Qt.AlignTop,self.rslt_list[17][18*i:18*(i+1)])

            x += 36
            death_date = self.rslt_list[13].split('/')[0]
            qp.drawText(130, x, 100, 30, Qt.AlignCenter,self.rslt_list[10])
            qp.drawText(290, x, 120, 30, Qt.AlignCenter,death_date)
            qp.drawText(470, x, 240, 30, Qt.AlignCenter,self.rslt_list[14])

            x += 36
            death_reason_len = len(self.rslt_list[22])
            if death_reason_len < 16:
                qp.drawText(130, x, 220, 30, Qt.AlignCenter,self.rslt_list[22])
            else:
                for i in range(death_reason_len%16):
                    qp.drawText(140, x + 5 + 15*i, 220, 25, Qt.AlignLeft|Qt.AlignTop,self.rslt_list[22][i*16:(i+1)*16])

            qp.drawText(410, x, 120, 30, Qt.AlignCenter,self.rslt_list[19])
            qp.drawText(590, x, 120, 30, Qt.AlignCenter,self.rslt_list[20])

            x += 36
            qp.drawText(130, x, 220, 30, Qt.AlignCenter,self.rslt_list[21])

            x += 36
            qp.drawText(80,x+35,300,30,Qt.AlignRight,self.rslt_list[33])


    def change_date(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month).zfill(2) +'月'+str(date.day).zfill(2)+'日'
        # return str(date.year)+'  '+ str(date.month).zfill(2) +'  '+str(date.day).zfill(2)

    def change_datetime(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1, 0, 0) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month).zfill(2) +'月'+str(date.day).zfill(2)+'日/' + str(date.hour).zfill(2) +'时' +str(date.minute).zfill(2) +'分'
        # return str(date.year)+'  '+ str(date.month).zfill(2) +'  '+str(date.day).zfill(2)+'  /' + str(date.hour).zfill(2) +'  ' +str(date.minute).zfill(2)

class Print_Setting(QWidget):

    printer_signal = pyqtSignal(str)

    def __init__(self):
        super(Print_Setting, self).__init__()
        self.setWindowTitle("打印机设置")
        self.setFixedSize(300, 200)
        self.set_ui()

    def set_ui(self):
        printers =  win32print.EnumPrinters(2)
        current_printer = win32print.GetDefaultPrinter()
        printers_list = [i[2] for i in printers]
        self.current_printer_label = QLabel("默认打印机")
        self.current_printer = QLineEdit(current_printer)
        self.current_printer.setReadOnly(True)
        self.current_printer.setStyleSheet("background:#f0f0f0")
        self.printer_label = QLabel("选择打印机")
        self.printer_name = QComboBox()
        for i in printers_list:
            self.printer_name.addItem(i)
        self.printer_name.currentIndexChanged.connect(self.change_printer)
        self.confirm_bnt = QPushButton("确定")
        # self.cancel_bnt = QPushButton("取消")
        self.confirm_bnt.clicked.connect(self.choose_printer)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.printer_label)
        self.layout.addWidget(self.printer_name)
        self.layout.addWidget(self.current_printer_label)
        self.layout.addWidget(self.current_printer)
        self.layout.addStretch()
        self.layout.addWidget(self.confirm_bnt)
        self.setLayout(self.layout)

    def change_printer(self):
        self.current_printer.setText(self.printer_name.currentText())

    def choose_printer(self):
        self.printer_signal.emit(self.current_printer.text())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = PrintWindow('20181026094542501',1)
    # mainwindow.print_data_bnt.clicked.connect(mainwindow.print_page1_data)
    mainwindow.show()
    sys.exit(app.exec_())
