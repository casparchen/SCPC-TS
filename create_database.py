from application import db
from application.models import User
import datetime


print 'Clearing old database...'
db.drop_all()

print 'create tables'
db.create_all()

print 'adding user'

u = User('1','1','1','1', datetime.datetime.utcnow())

db.session.add(u)
db.session.commit()