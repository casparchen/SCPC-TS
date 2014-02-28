#coding=utf-8

from application import db
from application.models import User, News, Problem, Submission, Contest, Forum
from datetime import datetime

print 'Clearing old database...'
db.drop_all()

print 'create tables'
db.create_all()

print 'adding user'
users = []
for i in range(20):
    u = User(u'user' + str(i),u'password' + str(i),u'admin@mrchenyi.com' + str(i),u'20081816' + str(i), datetime.now())
    users.append(u)

for i in range(20):
    db.session.add(users[i])
chenyi = User('admin', '123456', 'qq@qq.com', 'scpc_oj_username', datetime.now())
chenyi.group = "admin|user|manage user|manage problem|manage contest|manage news"
db.session.add(chenyi)

print 'adding news'
news = []
for i in range(10):
    n = News(datetime.now(), u"新闻标题新闻标题新闻 " + str(i), u"新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!")
    db.session.add(n)



print "adding problems"
p = None
for i in range(1):
    p = Problem(None, None, u"PKUOJ", u"1000", u"A + B Problem " + str(i), u"128k", u"1s", u"description", u"input", u"output", u"sample_input", u"sample_output", u"hint")
    db.session.add(p)

print "adding Contests"
p1 = None
for i in range(11):
    p1 = Contest(u"contests" + str(i), u"1000", datetime.utcnow(), datetime.utcnow(),"110|101|110",False, u"a|b|c|d|e", u"description")
    db.session.add(p1)


print "adding submission"
for i in range(5):
    s = Submission(users[5], p, datetime.now(), 'g++', '#include<stdio.h>\nint main(){\nint a,b;\nwhile(scanf(\"%d%d\",&a,&b)!=EOF){\nprintf(\"%d\\n\",a+b);\n}\n}\n', 'pending', None, None, 0, p.original_oj,p.original_oj_id)
    db.session.add(s)

print "adding forum.posts"
for i in range(20):
    po = Forum("title", "content", datetime.now(), 0, chenyi, None)
    db.session.add(po)

print "commiting..."
db.session.commit()





