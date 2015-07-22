#!/usr/bin/env python2.7.6
#-*-coding:utf-8-*-

#from sqlalchemy import create_engine
from sqlalchemy import *

# 创建engine
mysql_engine = create_engine('mysql://root:cecgw@localhost/my_db')  
#mysql_engine.connect()   
metadata = MetaData()

#创建users表
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(20), nullable = False),
    Column('age', Integer, nullable = False),
    Column('fullname', String(20), nullable = False),
    Column('password', String(20), nullable = False),
    mysql_engine='InnoDB'
)

#mysql_engine='InnoDB' 或者 mysql_engine='MyISAM' 表类型
metadata.create_all(mysql_engine)

