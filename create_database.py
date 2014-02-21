#coding=utf-8

from application import db
from application.models import User, News
from datetime import datetime

print 'Clearing old database...'
db.drop_all()

print 'create tables'
db.create_all()

print 'adding user'
u = User('chenyi','password','admin@mrchenyi.com','20081816', datetime.utcnow())
u1 = User('Liusx','password2','asdasd@qq.com','lsx', datetime.utcnow())
db.session.add(u)
db.session.add(u1)

print 'adding news'
n1 = News(datetime.utcnow(), u"SCPC TS系统正在制作中", "welcome!")
db.session.add(n1)

db.session.commit()




