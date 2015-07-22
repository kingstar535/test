#!/usr/bin/env python2.7.6
#-*-coding:utf-8-*-

#from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *

# 创建engine
#DB_CONNECT_STRING 就是连接数据库的路径。
DB_CONNECT_STRING = 'mysql://root:cecgw@localhost/my_db?charset=utf8'
# create_engine() 会返回一个数据库引擎，echo 参数为 True 时，会显示每条执行的 SQL 语句，生产环境下可关闭。
engine = create_engine(DB_CONNECT_STRING)  

#映射表类的父级，这个所谓的父级在背后会为子类的映射类做很多工作。
Base = declarative_base()
#declarative_base() 创建了一个 Base 类，这个类的子类可以自动与一个表关联。以Student 类为例，它的 __tablename__ 属性就是数据库中该表的名称，

#创建student表
class Student(Base):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    __tablename__='student'
    #这里定义数据项，不过不难看出的是Column绝对也附带了设置property()的操作，当你访问对应的属性时也会激活潜藏在Base中的相关方法
    id = Column(Integer,primary_key=True)
    name = Column(String(200))
    fullname = Column(String(200))
    password = Column(String(200))

    #这个对于定义student表不是必须的。
    #主要是用于后面添加student数据时用
    def __init__(self,name,fullname,password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<Student('%s','%s','%s')>" % (self.name,self.fullname,self.password)  


class Address(Base):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset':'utf8'
    }
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id')) #外键声明
    
    #建立关系。
    user = relationship("Student", backref=backref('address', order_by=id))

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address


def init_db():
    #Base.metadata.create_all(engine) 会找到 Base 的所有子类，并在数据库中建立这些表；drop_all() 则是删除这些表。
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

#执行建表语句（数据库需要自己建立），并通过数据库引擎engine写入数据,这句话可以反复执行
init_db()
  
#sessionmaker() 会生成一个数据库会话类。这个类的实例可以当成一个数据库连接，它同时还记录了一些查询的数据，并决定什么时候执行 SQL 语句。
#根据数据库引擎engine产生会话类
Session = sessionmaker(bind=engine)

#建立一个会话
session = Session()

session.execute("show databases")
#创建一条记录
ed_user = Student('ed', 'Ed Jones', 'edspassword')
#添加多条记录，这里还未提交到数据库
session.add(ed_user)

session.add_all([
    Student('wendy', 'Wendy Williams', 'foobar'),
    Student('mary', 'Mary Contrary', 'xxg527'),
    Student('fred', 'Fred Flinstone', 'blah')])

#提交数据到数据库(执行成功后就可以在数据中查看到数据了）
session.commit()

#查询操作
session.query(Student)

#对数据进行修改    
ed_user.password='newpassword'
#查看数据变更记录
print session.dirty
print session.new

#查询操作select Student.name,Student.fullname from Student
for row in session.query(Student.name,Student.fullname):
    print row.name,row.fullname

#查询操作select *,name from Student。all()方法可以将查询出来的结果转换成list类型，另外还有first,one等方法
for row in session.query(Student,Student.name).all():
    print row.name 

#统计结果
print session.query(Student,Student.name).all().count

#别名查询select name as name_label---重点注意新出现的name_label（只有动态语言才办得到的特性）
for row in session.query(Student.name.label('name_label')).all(): 
    print row.name_label

#指定结果集起止条数（分页用的着）select name from Student limits 1,3
for row in session.query(Student).order_by(Student.id)[1:3]:
    print row.name,row.fullname,row.password

#条件查询select name from Student where fullname='Ed Jones'
for row in session.query(Student.name).filter_by(fullname='Ed Jones'):
    print row.name
    
#多条件查询select * from Student where name='ed' and fullname='Ed Jones'
for row in session.query(Student).filter(Student.name=='ed').filter(Student.fullname=='Ed Jones'):
    print row.name,row.fullname,row.password

#session.delete(ed_user)
#session.commit()

# 关闭session
#session.close()
