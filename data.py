#!/usr/bin/env python
# coding:utf-8

import sqlite3


class Create():
    con = sqlite3.connect(".base.db")
    cur = con.cursor()

    user_sql = '''CREATE TABLE IF NOT EXISTS  user (
                    id int not null,
                    name text not null,
                    hospital_id int not null,
                    is_admin boolean not null,
                    is_delete boolean not null
            );
            '''
    hospital_sql = '''CREATE TABLE IF NOT EXISTS hospital (
                    id int not null,
                    name text not null,
                    code int not null,
                    depart_code text not null,
                    is_delete boolean not null
            );
           '''

class Data():
    pass
