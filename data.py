#!/usr/bin/env python
# coding:utf-8

import sqlite3


class Create():

    def __init__(self):

        self.con = sqlite3.connect("base.db")
        self.cur = self.con.cursor()

        user_sql = '''CREATE TABLE IF NOT EXISTS  user (
                        username text not null ,
                        nickname text not null,
                        password text not null,
                        hospital_id int not null,
                        account_level int not null,
                        is_delete int not null,
                        primary key (username)
               );'''
        hospital_sql = '''CREATE TABLE IF NOT EXISTS hospital (
                        id int not null,
                        name text not null,
                        code int not null,
                        depart_code text not null,
                        is_delete int not null,
                        reporter text not null,
                        primary key (id)
               ); '''
        bianhao_sql = '''CREATE TABLE IF NOT EXISTS bianhao (
                       hospital_id int not null,
                       last_id text not null,
                       last_year int not null,
                       last_number int not null,
                       primary key (hospital_id)
               );'''
        gender_sql = '''CREATE TABLE IF NOT EXISTS gender (
                        gender_serial int not null,
                        gender_name text not null,
                        primary key (gender_serial)
               );'''
        occupation_sql = '''CREATE TABLE IF NOT EXISTS occupation (
                        occupation_serial int not null,
                        occupation_name text not null,
                        primary key (occupation_serial)
               );'''
        race_sql = '''CREATE TABLE IF NOT EXISTS race (
                        race_serial int not null,
                        race_name text not null,
                        primary key (race_serial)
               );'''
        # race_sql_initial = '''INSERT INTO race VALUES (1,''),'''
        marriage_sql = '''CREATE TABLE IF NOT EXISTS marriage (
                        marriage_serial int not null,
                        marriage_name  text not null,
                        primary key (marriage_serial)
               );'''
        education_sql = '''CREATE TABLE IF NOT EXISTS education (
                        education_serial int not null,
                        education_name text not null,
                        primary key (education_serial)
               );'''
        death_point_sql = '''CREATE TABLE IF NOT EXISTS death_point (
                        death_point_serial int not null,
                        death_point_name text not null,
                        primary key (death_point_serial)
               );'''
        diagnost_hospital_sql = '''CREATE TABLE IF NOT EXISTS diagnost_hospital (
                        diagnost_hospital_serial int not null,
                        diagnost_hospital_name text not null,
                        primary key (diagnost_hospital_serial)
               );'''
        diagnost_method_sql = '''CREATE TABLE IF NOT EXISTS diagnost_method (
                        diagnost_method_serial int not null,
                        diagnost_method_name text not null,
                        primary key (diagnost_method_serial)
               );'''
        death_info_sql = '''CREATE  TABLE IF NOT EXISTS death_info (
                        report_distinct_code text not null,
                        report_department    text not null,
                        serial_number        text not null,
                        bianhao              text not null,
                        name                 text not null,
                        gender_code          int  not null,
                        race_code            int  not null,
                        id_class             text not null,
                        id                   text not null,
                        birthday             int  not null,
                        age                  text not null,
                        marriage_code        int  not null,
                        education_code       int  not null,
                        occupation_code      int  not null,
                        address_now          text not null,
                        code_now             int  not null,
                        address_birth        text not null,
                        code_birth           int  not null,
                        death_location       text not null,
                        death_location_code  int  not null,
                        company              text,
                        death_date           int  not null,
                        family               text,
                        familay_tel          text,
                        family_address       text,
                        disease_a            text not null,
                        disease_a_time       int,
                        disease_a_time_unit  text,
                        diseae_b             text,
                        disease_b_time       int,
                        disease_b_time_unit  text,
                        diseae_c             text,
                        disease_c_time       int,
                        disease_c_time_unit  text,
                        diseae_d             text,
                        disease_d_time       int,
                        disease_d_time_unit  text,
                        other_disease        text,
                        death_reason         text,
                        diagnost_department_code int,
                        diagnost_method_code int,
                        inhospital           text,
                        doctor               text,
                        regist_date          int,
                        reporter             text,
                        hospital             text,
                        hospital_code        text,
                        backup               text,
                        research             text,
                        researcher           text,
                        relation             text,
                        researcher_address   text,
                        death_reason2        text,
                        research_date        int,
                        primary key (serial_number)
               );'''
        self.cur.execute(user_sql)
        self.cur.execute(hospital_sql)
        self.cur.execute(bianhao_sql)
        self.cur.execute(gender_sql)
        self.cur.execute(occupation_sql)
        self.cur.execute(race_sql)
        self.cur.execute(marriage_sql)
        self.cur.execute(education_sql)
        self.cur.execute(death_point_sql)
        self.cur.execute(diagnost_hospital_sql)
        self.cur.execute(diagnost_method_sql)
        self.cur.execute(death_info_sql)
        rslt = self.cur.execute("select * from gender").fetchall()
        if not rslt:
            self.initial()
        else:
            pass
        self.con.close()

    def initial(self):
        gender_sql_initial = '''INSERT INTO gender values (1,'男'),(2,'女'),(3,'未知的性别'),(4,'未说明的性别');'''
        occupation_sql_initial = '''INSERT INTO occupation values (1,'公务员'),(2,'专业技术人员'),(3,'职员'),(4,'企业管理者'),(5,'工人'),(6,'农民'),(7,'学生'),
                                            (8,'现役军人'),(9,'自由职业者'),(10,'个体经营者'),(11,'无业人员'),(12,'离退休人员'),(13,'其他');'''
        marriage_sql_initial = '''INSERT INTO marriage VALUES (1,'未婚'),(2,'已婚'),(3,'丧偶'),(4,'离婚'),(5,'未说明');'''
        education_sql_initial = '''INSERT INTO education VALUES (1,'研究生'),(2,'大学'),(3,'大专'),(4,'中专'),(5,'技校'),(6,'高中'),(7,'初中及以下');'''
        death_point_sql_initial = '''INSERT INTO death_point VALUES (1,'医疗卫生机构'),(2,'来院途中'),(3,'家中'),(4,'养老服务机构'),(5,'其他场所'),(6,'不详');'''
        diagnost_hospital_sql_initial = '''INSERT INTO diagnost_hospital VALUES (1,'三级医院'),(2,'二级医院'),(3,'乡镇卫生院或社区卫生服务中心'),(4,'村卫生室'),(5,'其他医疗卫生机构'),(6,'未就诊');'''
        diagnost_method_sql_initial = '''INSERT INTO diagnost_method VALUES (1,'尸检'),(2,'病理'),(3,'手术'),(4,'临床+理化'),(5,'临床'),(6,'死后推断'),(7,'不详')'''
        user_initial = '''INSERT INTO user VALUES ('admin', 'admin', '202cb962ac59075b964b07152d234b70',0,9,0)'''
        hospital_initial = '''INSERT INTO hospital VALUES (0,'admin',00000000,'000000',0,'admin')'''
        race_list = [(0,"汉族"),(1,"蒙古族"),(2,"回族"),(3,"藏族"),(4,"维吾尔族 "),
                    (5,"苗族"),(6,"彝族"),(7,"壮族"),(8,"布依族"),(9,"朝鲜族"),(10,"满族"),
                    (11,"侗族"),(12,"瑶族"),(13,"白族"),(14,"土家族"),(15,"哈尼族"),(16,"哈萨克族"),(17,"傣族"),(18,"黎族"),(19,"傈傈族 "),
                    (22,"高山族"),(23,"拉祜族"),(24,"水族"),(25,"东乡族"),(26,"纳西族"),(27,"景颇族"),(28,"柯尔克孜族"),(29,"土族"),
                    (30,"达斡尔族"),(31,"仫佬族"),(32,"羌族"),(33,"布朗族"),(34,"撒拉族"),(35,"毛南族"),(36,"仡佬族"),(37,"锡伯族"),
                    (38,"阿昌族"),(39 ," 普米族"),(40,"怒族"),(41,"乌孜别克族"),(42,"俄罗斯族"),(43,"鄂温克族"),(44,"德昂族"),
                    (45,"保安族"),(46,"裕固族"),(47,"京族 "),(48,"塔塔尔族"),(49,"独龙族"),(50,"鄂伦春族"),(51 ,"赫哲族"),
                    (52,"门巴族"),(53,"珞巴族"),(54,"基诺族"),(55,"外国血统中国籍人士"),(56,"其他"),(57 ,"不详")]
        race_initial_sql = '''INSERT INTO race VALUES (?,?)'''
        self.cur.execute(gender_sql_initial)
        self.cur.execute(occupation_sql_initial)
        self.cur.execute(marriage_sql_initial)
        self.cur.execute(education_sql_initial)
        self.cur.execute(death_point_sql_initial)
        self.cur.execute(diagnost_hospital_sql_initial)
        self.cur.execute(diagnost_method_sql_initial)
        self.cur.execute(user_initial)
        self.cur.execute(hospital_initial)
        self.cur.executemany(race_initial_sql, race_list)
        self.con.commit()


class DataBase():
    def __init__(self):
        self.con = sqlite3.connect('base.db')
        self.cur = self.con.cursor()

if __name__ == '__main__':
    a = Create()
