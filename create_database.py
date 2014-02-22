#coding=utf-8

from application import db
from application.models import User, News, Problem, Submission
from datetime import datetime

print 'Clearing old database...'
db.drop_all()

print 'create tables'
db.create_all()

print 'adding user'
users = []
for i in range(20):
    u = User(u'user' + str(i),u'password' + str(i),u'admin@mrchenyi.com' + str(i),u'20081816' + str(i), datetime.utcnow())
    users.append(u)

for i in range(20):
    db.session.add(users[i])

print 'adding news'
news = []
for i in range(20):
    n = News(datetime.utcnow(), u"新闻标题新闻标题新闻 " + str(i), u"新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!新闻内容!")
    news.append(n)

for i in range(20):
    db.session.add(news[i])


print "adding problems"
problems = []
for i in range(20):
    p = Problem(None, None, u"original_oj", u"Problem " + str(i), u"128k", u"1s", u"description", u"input", u"output", u"sample_input", u"sample_output", u"hint")
    problems.append(p)

for i in range(20):
    db.session.add(problems[i])

print "adding submission"
submissions = []
for i in range(20):
    s = Submission(users[5], problems[1], datetime.utcnow(), 'C', 'print(123)', 'pending', None, None, 0)
    db.session.add(s)

db.session.commit()





