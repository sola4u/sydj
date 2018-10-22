
#/usr/bin/env python
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
import sys
import platform


class PrintWindow(QWidget):

    def __init__(self, id):
        super(PrintWindow, self).__init__()
        # self.setFixedSize(810, 700)
        self.resize(810, 700)
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.img = QImage()
        self.id = id
        self.set_ui()

    def  set_ui(self):
        self.layout = QVBoxLayout()

        self.print_bnt = QPushButton("打印")
        self.print_bnt2 = QPushButton("仅打印数据")
        self.close_bnt = QPushButton('关闭')
        self.to_page2_bnt = QPushButton("查看第二联")
        self.save_page1_bnt = QPushButton("save page1")
        self.print_bnt.clicked.connect(self.print_page1)
        self.print_bnt2.clicked.connect(self.print_page1_data)
        self.close_bnt.clicked.connect(self.close_page)
        self.to_page2_bnt.clicked.connect(self.to_page2)
        self.save_page1_bnt.clicked.connect(self.save_page1)

        self.pic = PaintArea(self.id)

        # self.a = QLabel()
        # self.a.setPixmap(QPixmap('1.png'))

        self.bnt_layout = QHBoxLayout()
        self.bnt_layout.addStretch(4)
        self.bnt_layout.addWidget(self.to_page2_bnt)
        self.bnt_layout.addWidget(self.print_bnt)
        self.bnt_layout.addWidget(self.print_bnt2)
        self.bnt_layout.addWidget(self.save_page1_bnt)
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

    def print_page1(self):
        plat_form = platform.platform()
        if 'Windows' in plat_form:
            import win32print
            import win32api
            currentprinter = win32print.GetDefaultPrinter()
            win32api.ShellExecute(0,'print','tmp.png','/d:%s'%currentprinter,'.',0)
        else:
            pass

    def print_page1_data(self):
        # self.printer.setOutputFormat(QPrinter.PdfFormat)
        # self.printer.setOutputFileName('a.pdf')
        pass


    def close_page(self):
        self.close()

    def to_page2(self):
        pass

    def save_page1(self):
        filename,ok = QFileDialog.getSaveFileName(self,'savefile','.')
        print(filename,ok)

class PaintArea(QWidget):

    def __init__(self,id):
        super(PaintArea, self).__init__()
        self.id= str(id)
        self.setFixedSize(760, 1080)
        # self.printer = QPrinter()

    def paintEvent(self, event):
        map = QPixmap(800, 1080)
        map.fill(Qt.white)
        qp = QPainter(map)
        # self.printer.setOutputFormat(QPrinter.PdfFormat)
        # self.printer.setOutputFileName('./tmp.pdf')
        # qp = QPainter(self.printer)
        qp.begin(self)
        self.drawPic(event, qp)
        qp.end()
        map.save('tmp.png','PNG')

    def drawPic(self,event, qp):
        self.db = DataBase()
        self.db.cur.execute("select * from death_info where  serial_number = '%s'"%(self.id))
        self.rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.list_dic = Choice_Dic()
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
            diagnost_department = self.list_dic.diagnost_department_list[self.rslt[40]]
            diagnost_method = self.list_dic.diagnost_method_list[self.rslt[41]]
            rslt_list = [address,self.rslt[1],self.rslt[4],self.rslt[5],gender,race,id_class,self.rslt[9],
                        self.rslt[11],marriage,self.change_date(self.rslt[10]),education,occupation,
                        self.change_date(self.rslt[21]),death_location,'否',self.rslt[20],self.rslt[17],
                        self.rslt[15],self.rslt[22], self.rslt[23],self.rslt[24],self.rslt[25],str(self.rslt[26])+self.rslt[27],
                        self.rslt[28],str(self.rslt[29])+self.rslt[30], self.rslt[31], str(self.rslt[32])+self.rslt[33],
                        self.rslt[34], str(self.rslt[35])+self.rslt[36],self.rslt[37],diagnost_department,diagnost_method,
                        self.change_date(self.rslt[44]),self.rslt[38],self.rslt[39],self.rslt[48],self.rslt[49],self.rslt[50],
                        self.rslt[52],self.rslt[51],self.rslt[53],self.change_date(self.rslt[54])]

        qp.setPen(QPen(Qt.black,1))
        qp.setFont(QFont('宋体', 16,QFont.Bold))
        qp.drawText(0,65,800,50, Qt.AlignCenter, "居民死亡医学证明（推断）书")
        qp.setFont(QFont('宋体', 9))
        qp.drawText(50,110,800,14.2, Qt.AlignLeft, rslt_list[0])
        qp.drawText(50,128,450,23.9, Qt.AlignLeft, "行政区划代码 %s"%(rslt_list[1]))
        qp.drawText(450,128,310,23.9, Qt.AlignLeft, "编号：%s"%(rslt_list[2]))
        x = 140
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,144,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,124,36)
        qp.drawRect(438,x,56,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,66,36)
        qp.drawRect(644,x,84,36)
        qp.drawText(40,x,75,30, Qt.AlignCenter,'死者姓名')
        qp.drawText(115,x,144,30, Qt.AlignCenter,rslt_list[3])
        qp.drawText(259,x,55,30,Qt.AlignCenter,'性别')
        qp.drawText(314,x,124,30,Qt.AlignCenter,rslt_list[4])
        qp.drawText(438,x,56,30,Qt.AlignCenter,'民族')
        qp.drawText(494,x,84,30,Qt.AlignCenter,rslt_list[5])
        qp.drawText(578,x,66,20,Qt.AlignCenter,'国家或')
        qp.drawText(578,x,66,50,Qt.AlignCenter,'地区')
        qp.drawText(644,x,84,30,Qt.AlignCenter,'中国')

        x += 36
        qp.drawRect(40,x,75,68)
        qp.drawRect(115,x,144,68)
        qp.drawRect(259,x,55,68)
        qp.drawRect(314,x,124,68)
        qp.drawRect(438,x,56,68)
        qp.drawRect(494,x,84,68)
        qp.drawRect(578,x,66,68)
        qp.drawRect(644,x,84,68)
        qp.drawText(40,x,75,40,Qt.AlignCenter,'有效身份')
        qp.drawText(40,x,75,80,Qt.AlignCenter,'证件类别')
        qp.drawText(115,x,144,65, Qt.AlignCenter,rslt_list[6])
        qp.drawText(259,x,55,40,Qt.AlignCenter,'证件')
        qp.drawText(259,x,55,80,Qt.AlignCenter,'号码')
        qp.drawText(314,x,124,65,Qt.AlignCenter,rslt_list[7])
        qp.drawText(438,x,56,65,Qt.AlignCenter,'年龄')
        qp.drawText(494,x,84,65,Qt.AlignCenter,rslt_list[8])
        qp.drawText(578,x,66,40,Qt.AlignCenter,'婚姻')
        qp.drawText(578,x,66,80,Qt.AlignCenter,'状况')
        qp.drawText(644,x,84,65,Qt.AlignCenter,rslt_list[9])

        x += 68
        qp.drawRect(40,x,75,68)
        qp.drawRect(115,x,144,68)
        qp.drawRect(259,x,55,68)
        qp.drawRect(314,x,124,68)
        qp.drawRect(438,x,56,68)
        qp.drawRect(494,x,234,68)
        qp.drawText(40,x+5,75,35,Qt.AlignCenter,'出生')
        qp.drawText(40,x+5,75,65,Qt.AlignCenter,'日期')
        qp.drawText(115,x,144,65, Qt.AlignCenter,rslt_list[10])
        qp.drawText(259,x,55,40,Qt.AlignCenter,'文化')
        qp.drawText(259,x,55,80,Qt.AlignCenter,'程度')
        qp.drawText(314,x,124,65,Qt.AlignCenter,rslt_list[11])
        qp.drawText(438,x,56,40,Qt.AlignCenter,'个人')
        qp.drawText(438,x,56,80,Qt.AlignCenter,'身份')
        qp.drawText(494,x,234,65,Qt.AlignCenter,rslt_list[12])

        x += 68
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,144,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,180,36)
        qp.drawRect(494,x,150,36)
        qp.drawRect(644,x,84,36)
        qp.drawText(40,x,75,30,Qt.AlignCenter,'死亡日期')
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[13])
        qp.drawText(259,x,55,20,Qt.AlignCenter,'死亡')
        qp.drawText(259,x,55,50,Qt.AlignCenter,'地点')
        qp.drawText(314,x,180,30,Qt.AlignCenter,rslt_list[14])
        qp.drawText(494,x,150,20,Qt.AlignCenter,'死亡时是否处于妊娠期')
        qp.drawText(494,x,150,50,Qt.AlignCenter,'或妊娠终止后42天内')
        qp.drawText(644,x,84,30,Qt.AlignCenter,rslt_list[15])

        x += 36
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,144,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,180,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,20,Qt.AlignCenter,'生前')
        qp.drawText(40,x,75,50,Qt.AlignCenter,'工作单位')
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[16])
        qp.drawText(259,x,55,20,Qt.AlignCenter,'户籍')
        qp.drawText(259,x,55,50,Qt.AlignCenter,'地址')
        address_a_length = len(rslt_list[17])
        for i in range(address_a_length%14):
            qp.drawText(314,x,180,20+30*i,Qt.AlignCenter,rslt_list[17][14*i:14*(i+1)])
        qp.drawText(494,x,84,20,Qt.AlignCenter,'常住')
        qp.drawText(494,x,84,50,Qt.AlignCenter,'地址')
        address_b_length = len(rslt_list[18])
        for i in range(address_b_length%11):
            qp.drawText(578,x,150,20+30*i,Qt.AlignCenter,rslt_list[18][11*i:11*(i+1)])

        x += 36
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,144,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,180,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,20,Qt.AlignCenter,'可联系的')
        qp.drawText(40,x,75,50,Qt.AlignCenter,'家属姓名')
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[19])
        qp.drawText(259,x,55,20,Qt.AlignCenter,'联系')
        qp.drawText(259,x,55,50,Qt.AlignCenter,'电话')
        qp.drawText(314,x,180,30,Qt.AlignCenter,rslt_list[20])
        qp.drawText(494,x,84,20,Qt.AlignCenter,'家属住址')
        qp.drawText(494,x,84,50,Qt.AlignCenter,'或工作单位')
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[21])

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'致死的主要疾病诊断')
        qp.drawText(259,x,319,30,Qt.AlignCenter,'疾病名称(勿填症状体征)')
        qp.drawText(578,x,150,30,Qt.AlignCenter,'发病至死亡大概间隔时间')

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'Ⅰ.(a)直接死亡原因')
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[22])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[23])


        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'(b)引起(a)的疾病或情况')
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[24])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[25])

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'(c)引起(b)的疾病或情况')
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[26])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[27])

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'(d)引起(c)的疾病或情况')
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[28])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[29])

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,319,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,20,Qt.AlignCenter,'Ⅱ.其他疾病诊断(促进死亡，但与')
        qp.drawText(40,x,219,50,Qt.AlignCenter,'导致死亡无关的其他重要情况)')
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[30])
        qp.drawText(578,x,150,30,Qt.AlignCenter,'')

        x += 36
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,379,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,20,Qt.AlignCenter,'生前主要疾病')
        qp.drawText(40,x,74,50,Qt.AlignCenter,'最高诊断单位')
        qp.drawText(115,x,379,30,Qt.AlignCenter,rslt_list[31])
        qp.drawText(494,x,84,20,Qt.AlignCenter,'生前主要疾病')
        qp.drawText(494,x,84,50,Qt.AlignCenter,'最高诊断依据')
        qp.drawText(578,x,150,36,Qt.AlignCenter,rslt_list[32])

        x += 36
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,144,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,180,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,30,Qt.AlignCenter,'医师签名')
        qp.drawText(259,x,55,20,Qt.AlignCenter,'医疗卫生')
        qp.drawText(259,x,55,50,Qt.AlignCenter,'机构盖章')
        qp.drawText(494,x,84,30,Qt.AlignCenter,'填表日期')
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[33])

        x += 36
        qp.drawRect(40,x,219,36)
        qp.drawRect(259,x,235,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,219,30,Qt.AlignCenter,'(以下由编码人员填写)根本死亡原因:')
        qp.drawText(259,x,235,30,Qt.AlignCenter,rslt_list[34])
        qp.drawText(494,x,84,30,Qt.AlignCenter,'ICD编码:')
        qp.drawRect(578,x,150,36)
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[35])

        x += 36
        qp.setFont(QFont('宋体', 14,QFont.Bold))
        qp.drawText(40,x,688,40,Qt.AlignCenter,'死亡调查记录')
        qp.setFont(QFont('宋体', 9))

        x += 40
        qp.drawRect(40,x,688,128)
        qp.drawText(40,x,180,36,Qt.AlignCenter,'死者生前病史及症状体征:')
        research_len = len(rslt_list[36])
        for i in range(research_len%55):
            qp.drawText(60,x+30*(1+i),700,36,Qt.AlignLeft,rslt_list[36][i*55:(i+1)*55])
        qp.drawText(438,x+110,250,36,Qt.AlignLeft,'以上情况属实，被调查者签字:')

        x += 128
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,100,36)
        qp.drawRect(215,x,44,36)
        qp.drawRect(259,x,55,36)
        qp.drawRect(314,x,80,36)
        qp.drawRect(394,x,100,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,20,Qt.AlignCenter,'被调查者')
        qp.drawText(40,x,75,50,Qt.AlignCenter,'姓名')
        qp.drawText(115,x,100,30,Qt.AlignCenter,rslt_list[37])
        qp.drawText(215,x,44,20,Qt.AlignCenter,'与死者')
        qp.drawText(215,x,44,50,Qt.AlignCenter,'关系')
        qp.drawText(259,x,55,30,Qt.AlignCenter,rslt_list[38])
        qp.drawText(314,x,80,20,Qt.AlignCenter,'联系')
        qp.drawText(314,x,80,50,Qt.AlignCenter,'电话')
        qp.drawText(394,x,100,30,Qt.AlignCenter,rslt_list[39])
        qp.drawText(494,x,84,20,Qt.AlignCenter,'联系地址')
        qp.drawText(494,x,84,50,Qt.AlignCenter,'或工作单位')
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[40])

        x +=36
        qp.drawRect(40,x,75,36)
        qp.drawRect(115,x,199,36)
        qp.drawRect(314,x,80,36)
        qp.drawRect(394,x,100,36)
        qp.drawRect(494,x,84,36)
        qp.drawRect(578,x,150,36)
        qp.drawText(40,x,75,30,Qt.AlignCenter,'死因推断')
        qp.drawText(115,x,199,30,Qt.AlignCenter,rslt_list[41])
        qp.drawText(314,x,80,30,Qt.AlignCenter,'被调查者签名')
        qp.drawText(494,x,84,30,Qt.AlignCenter,'调查日期')
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[42])

        x += 36
        qp.drawText(40,x,688,30,Qt.AlignLeft,'注：①此表填写范围为在家、养老服务机构、其他场所正常死亡镇；②被调查者应为死者近亲或知情人；③调查时应出具以下资料:')

        x += 20
        qp.drawText(40,x,688,30,Qt.AlignLeft,'被调查者有效身份证件，居住地居委会或村委会证明，死者身份证和/或户口簿、生前病史卡.')

    def change_date(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month) +'月'+str(date.day)+'日'

class SavePage1(QWidget):

    def __init__(self, id):
        super(SavePage1, self).__init__()
        self.id = id
        self.set_ui()

    def set_ui(self):
        self.a = DrawPage1(self.id)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.a)
        self.setLayout(self.layout)

class DrawPage1(PaintArea):

    def __init__(self, id):
        super(DrawPage1, self).__init__(id)
        self.id = id

    def paintEvent(self, event):
        map = QPixmap(800, 1080)
        map.fill(Qt.white)
        qp = QPainter(map)
        qp.begin(self)
        self.drawPic(event, qp)
        qp.end()
        # a = rslt_list[3] + rslt_list[6]
        map.save('%s.png'%('a'),'PNG')

    def drawPic(self, event, qp):
        PaintArea.drawPic(self, event, qp)


class PaintPage1Data(QWidget):

    def __init__(self,id):
        super(PaintPage1Data,self).__init__()
        self.id = id
        self.setFixedSize(760, 1080)
        self.printer= QPrinter()
        self.printer.setPageSize(QPrinter.A4)

    def paintEvent(self, event):
        qp = QPainter(self.printer)
        self.drawText(event, qp)

    def drawText(self,event, qp):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            return
        self.db = DataBase()
        self.db.cur.execute("select * from death_info where  serial_number = '%s'"%(self.id))
        self.rslt = self.db.cur.fetchone()
        self.db.con.close()
        self.list_dic = Choice_Dic()
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
            diagnost_department = self.list_dic.diagnost_department_list[self.rslt[40]]
            diagnost_method = self.list_dic.diagnost_method_list[self.rslt[41]]
            rslt_list = [address,self.rslt[1],self.rslt[4],self.rslt[5],gender,race,id_class,self.rslt[9],
                        self.rslt[11],marriage,self.change_date(self.rslt[10]),education,occupation,
                        self.change_date(self.rslt[21]),death_location,'否',self.rslt[20],self.rslt[17],
                        self.rslt[15],self.rslt[22], self.rslt[23],self.rslt[24],self.rslt[25],str(self.rslt[26])+self.rslt[27],
                        self.rslt[28],str(self.rslt[29])+self.rslt[30], self.rslt[31], str(self.rslt[32])+self.rslt[33],
                        self.rslt[34], str(self.rslt[35])+self.rslt[36],self.rslt[37],diagnost_department,diagnost_method,
                        self.change_date(self.rslt[44]),self.rslt[38],self.rslt[39],self.rslt[48],self.rslt[49],self.rslt[50],
                        self.rslt[52],self.rslt[51],self.rslt[53],self.change_date(self.rslt[54])]

        qp.setPen(QPen(Qt.black,1))
        qp.setFont(QFont('宋体', 9))
        qp.drawText(50,110,800,14.2, Qt.AlignLeft, rslt_list[0])
        qp.drawText(100,128,450,23.9, Qt.AlignLeft, "%s"%(rslt_list[1]))
        qp.drawText(550,128,310,23.9, Qt.AlignLeft, "%s"%(rslt_list[2]))
        x = 145
        qp.drawText(115,x,144,30, Qt.AlignCenter,rslt_list[3])
        qp.drawText(314,x,124,30,Qt.AlignCenter,rslt_list[4])
        qp.drawText(494,x,84,30,Qt.AlignCenter,rslt_list[5])
        qp.drawText(644,x,84,30,Qt.AlignCenter,'中国')

        x += 36
        qp.drawText(115,x,144,65, Qt.AlignCenter,rslt_list[6])
        qp.drawText(314,x,124,65,Qt.AlignCenter,rslt_list[7])
        qp.drawText(494,x,84,65,Qt.AlignCenter,rslt_list[8])
        qp.drawText(644,x,84,65,Qt.AlignCenter,rslt_list[9])

        x += 68
        qp.drawText(115,x,144,65, Qt.AlignCenter,rslt_list[10])
        qp.drawText(314,x,124,65,Qt.AlignCenter,rslt_list[11])
        qp.drawText(494,x,234,65,Qt.AlignCenter,rslt_list[12])

        x += 68
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[13])
        qp.drawText(314,x,180,30,Qt.AlignCenter,rslt_list[14])
        qp.drawText(644,x,84,30,Qt.AlignCenter,rslt_list[15])

        x += 36
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[16])
        address_a_length = len(rslt_list[17])
        for i in range(address_a_length%14):
            qp.drawText(314,x,180,20+30*i,Qt.AlignCenter,rslt_list[17][14*i:14*(i+1)])
        address_b_length = len(rslt_list[18])
        for i in range(address_b_length%11):
            qp.drawText(578,x,150,20+30*i,Qt.AlignCenter,rslt_list[18][11*i:11*(i+1)])

        x += 36
        qp.drawText(115,x,144,30,Qt.AlignCenter,rslt_list[19])
        qp.drawText(314,x,180,30,Qt.AlignCenter,rslt_list[20])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[21])

        x += 36

        x += 36
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[22])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[23])

        x += 36
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[24])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[25])

        x += 36
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[26])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[27])

        x += 36
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[28])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[29])

        x += 36
        qp.drawText(259,x,319,30,Qt.AlignCenter,rslt_list[30])
        qp.drawText(578,x,150,30,Qt.AlignCenter,'')

        x += 36
        qp.drawText(115,x,379,30,Qt.AlignCenter,rslt_list[31])
        qp.drawText(578,x,150,36,Qt.AlignCenter,rslt_list[32])

        x += 36
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[33])

        x += 36
        qp.drawText(259,x,235,30,Qt.AlignCenter,rslt_list[34])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[35])

        x += 36

        x += 40
        research_len = len(rslt_list[36])
        for i in range(research_len%55):
            qp.drawText(60,x+30*(1+i),700,36,Qt.AlignLeft,rslt_list[36][i*50:(i+1)*50])

        x += 128
        qp.drawText(115,x,100,30,Qt.AlignCenter,rslt_list[37])
        qp.drawText(259,x,55,30,Qt.AlignCenter,rslt_list[38])
        qp.drawText(394,x,100,30,Qt.AlignCenter,rslt_list[39])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[40])

        x +=36
        qp.drawText(115,x,199,30,Qt.AlignCenter,rslt_list[41])
        qp.drawText(578,x,150,30,Qt.AlignCenter,rslt_list[42])

    def change_date(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month) +'月'+str(date.day)+'日'



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = PrintWindow('20180925145630743')
    mainwindow.show()
    sys.exit(app.exec_())
