
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


class PrintWindow(QWidget):

    def __init__(self,id):
        super(PrintWindow, self).__init__()
        self.id = id
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.setFixedSize(800,600)
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
            html_page1 = '''<style>
                            body {width:1075px; height:1567px;}
                            td {font-size:12px;text-align:center;border:1px solid red;}
                            p {font-size:12px;}
                            table {border:1px;border-collapse:collapse;}
                            span {padding-right:300px;}
                            tr {height:60px;}
                            </style>'''
            html_page1 += '''
                <body>
                <h1 align='center'>居民死亡医学证明（推断）书</h1>
                <p>{0}</p>
                <p><span colspan='4'>行政区划代码:{1}</span>
                   <span colspan='4' >编号：{2}</span>
                </p>
                <table border='1' border-collapse='collpase' cellspacing='0' cellpadding='1'>
                <tr>
                    <td width='11%'>死者姓名</td><td width='20%'>{3}</td>
                    <td width='7%'>性别</td><td width='17%'>{4}</td>
                    <td width='8%'>民族</td><td width='12%'>{5}</td>
                    <td width='8%'>国家或地区</td><td width='17%'>中国</td>
                </tr>
                <tr height='100'>
                    <td width='11%'>有效身份证件类别</td><td width='20%'>{6}</td>
                    <td width='7%'>证件号码</td><td width='17%'>{7}</td>
                    <td width='8%'>年龄</td><td width='12%'>{8}</td>
                    <td width='8%'>婚姻状况</td><td width='17%'>{9}</td>
                </tr>
                <tr height='100'>
                    <td width='11%'>出生日期</td><td width='20%'>{10}</td>
                    <td width='7%'>文化程度</td><td width='17%'>{11}</td>
                    <td width='8%'>个人身份</td><td width='37%' colspan = '3'>{12}</td>
                </tr>
                <tr>
                    <td width='11%'>死亡日期</td><td width='20%'>{13}</td>
                    <td width='7%'>死亡地点</td><td width='17%' colspan='2'>{14}</td>
                    <td width='20%' colspan = '2'>死亡时是否处于妊娠期或妊娠终止后42天内</td><td width='17%'>{15}</td>
                </tr>
                <tr>
                    <td width='11%'>生前工作单位</td><td width='20%'>{16}</td>
                    <td width='7%'>户籍地址</td><td width='17%' colspan='2'>{17}</td>
                    <td width='12%'>常住地址</td><td width='25%' colspan='2'>{18}</td>
                </tr>
                <tr>
                    <td width='11%'>可联系的家属姓名</td><td width='20%'>{19}</td>
                    <td width='7%'>联系电话</td><td width='17%' colspan='2'>{20}</td>
                    <td width='12%'>家属住址或工作单位</td><td width='25%' colspan='2'>{21}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>致死的主要疾病诊断</td>
                    <td width='44%' colspan='4'>疾病名称（勿填症状体征）</td>
                    <td width='15%' colspan='2'>发病至死亡大概间隔时间</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>Ⅰ.(a)直接死亡原因</td>
                    <td width='44%' colspan='4'>{22}</td>
                    <td width='15%' colspan='2'>{23}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>(b)引起(a)的疾病或情况</td>
                    <td width='44%' colspan='4'>{24}</td>
                    <td width='15%' colspan='2'>{25}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>(c)引起(b)的疾病或情况</td>
                    <td width='44%' colspan='4'>{26}</td>
                    <td width='15%' colspan='2'>{27}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>(d)引起(c)的疾病或情况</td>
                    <td width='44%' colspan='4'>{28}</td>
                    <td width='15%' colspan='2'>{29}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>Ⅱ.其他疾病诊断（促进死亡，但与导致死亡无关的其他重要情况）</td>
                    <td width='44%' colspan='4'>{30}</td>
                    <td width='15%' colspan='2'></td>
                </tr>
                <tr>
                    <td width ='31%'>生前主要疾病最高诊断单位</td><td width='52%' colspan='4'>{31}</td>
                    <td width='12%'>生前主要疾病最高诊断依据</td><td width='25%' colspan='2'>{32}</td>
                </tr>
                <tr>
                    <td width='11%'>医师签名</td><td width='20%'></td>
                    <td width='7%'>医疗卫生机构盖章</td><td width='17%' colspan='2'></td>
                    <td width='12%'>填表日期</td><td width='25%' colspan='2'>{33}</td>
                </tr>
                <tr>
                    <td width='31%' colspan='2'>（以下由编码人员填写）根本死亡原因：</td>
                    <td width='32%' colspan='3'>{34}</td>
                    <td width='37%' colspan='3' text-align='left'>ICD编码：</td>
                </tr>
                <tr>
                <td colspan='8'>
                <h2 align='center'>死亡调查记录</h2>
                </td>
                </tr>
                <tr height='150'>
                     <td colspan='8' align='left'>死者生前病史及症状体征:</td>
                </tr>
                <tr>
                    <td colspan='8' height='300'></td>
                </tr>
                <tr>
                    <td width='11%'>被调查者姓名</td><td width='13%'></td>
                    <td width='7%'>与死者关系</td><td width='7%'></td>
                    <td width='10%'>联系电话</td><td width='15%'></td>
                    <td width='12%'>联系地址或动作单位</td><td width='25%'></td>
                </tr>
                <tr>
                    <td width='11%'>死因推断</td><td width='27%' colspan='3'></td>
                    <td width='10%'>调查者签名</td><td width='15%'></td>
                    <td width='12%'>调查日期</td><td width='25%'></td>
                </tr>
                </table>
                <p> 注：①此表填写范围为在家、养老服务机构、其他场所正常死亡者；②被调查者应为死者近亲或知情人；③调查时应出具以下资料：被
                调查者有效身份证件，居住地居委会或村委会证明，死者身份证和/或户口簿、生前病史卡.</p>
                </body>
            '''.format(address,self.rslt[1],self.rslt[4],self.rslt[5],gender,race,id_class,self.rslt[9],
                        self.rslt[11],marriage,self.change_date(self.rslt[10]),education,occupation,
                        self.change_date(self.rslt[21]),death_location,'否',self.rslt[20],self.rslt[17],
                        self.rslt[15],self.rslt[22], self.rslt[23],self.rslt[24],self.rslt[25],str(self.rslt[26])+self.rslt[27],
                        self.rslt[28],str(self.rslt[29])+self.rslt[30], self.rslt[31], str(self.rslt[32])+self.rslt[33],
                        self.rslt[34], str(self.rslt[35])+self.rslt[36],self.rslt[37],diagnost_department,diagnost_method,
                        self.change_date(self.rslt[53]),self.rslt[38])
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
