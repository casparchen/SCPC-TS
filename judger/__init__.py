#coding=utf-8
import re,urllib,urllib2,cookielib,time
from application import db
from application.models import Submission
from judger.HDOJ import HDOJ
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
import threading
from flask_sqlalchemy import SQLAlchemy
from application import app

def daemon(th, timeout, account):
    try:
        th.setDaemon(True)
        th.start()
        th.join(timeout)
        th.stillRuning=False
        if th.done == False:
            print "[Task #%s]: rejudge."% th.submission.id 
            session = db.create_scoped_session()
            session.execute("update submission set judger_status=0 where id=%d" %  th.submission.id)
            session.flush()
            session.commit()
        #print "[Task #%s]: daemon killed or stoped." % th.submission.id
        account['used'] = False
    except Exception, e:
        print "Warning: __init__.daemon()"
        print e
    finally:
        global guard
        guard.remove_task(th.submission)
        th.account['used'] = False
        

class SCPC_Judger_Guard(object):
    """guard"""
    judgers = {}
    tasks = []
    MAX_JUDGE_TASK = 1

    def __init__(self, MAX_JUDGE_TASK):
        self.MAX_JUDGE_TASK = MAX_JUDGE_TASK

    def start(self):
        while True:
            #print "[Main] current tasks:" + str(len(self.tasks))
            time.sleep(3)
            if len(self.tasks) == self.MAX_JUDGE_TASK: continue
            submission = self.request_new_submission_by_databse()
            if submission is not None:
                self.tasks.append(submission)
                self.judge(submission)
            

    def judge(self, task):
        try:
            spare_account = self.request_spare_judger(task.original_oj)
            spare_account['used'] = True
            #print "[Main] select accout: ", spare_account['username']
            j = self.judgers[task.original_oj]['oj'](spare_account)
            
            dm = threading.Thread(target=daemon,args=(j.judge(task), 20, spare_account))
            #print "[Task #%s]: start daemon" % task.id
            dm.start()
        except Exception, e:
            print "Warning: __init__.judge()"
        


    def request_spare_judger(self, oj):
        for x in self.judgers[oj]['account']:
            if 'used' not in x:
                return x
            elif x['used'] == False:
                return x
        return None

    def request_new_submission_by_databse(self):
        try:
            """
            A = False
            B = False
            for x in self.judgers:
                if self.request_spare_judger(str(x)) != None:
                    A = or_(A, Submission.original_oj==str(x))
                    B = True
            if B != True: return None
            db.session.flush()
            submission = Submission.query.filter(and_(Submission.judger_status==0, A)).first()
            """
            session = db.create_scoped_session()
            submission = session.execute("select * from submission where judger_status=0 and original_oj='HDOJ' limit 1").first()
            if submission is not None:
                session.execute("update submission set judger_status=%d where id=%d" % (time.time(), submission.id))
            session.flush()
            session.commit()
            return submission
        except SQLAlchemyError, e:
            print "Warning: __init__.request_new_submission_by_databse()"
            print "rollback"
            db.session.rollback()
            print e
            return None
        except Exception, e:
            print "Warning: __init__.request_new_submission_by_databse()"
            print e
            return None
        

    def add_judger(self, judger):
        if judger['oj'].oj_name is not None and judger['oj'].oj_name != "":
            self.judgers[judger['oj'].oj_name] = judger

    def remove_task(self, task):
        print "[Task #%s]: Done." % task.id
        if task in self.tasks:
            self.tasks.remove(task)

guard = SCPC_Judger_Guard(2)

guard.add_judger({"oj" : HDOJ, "account": [{"username" : "scpc1", "password" : "swustscpc"}, {"username" : "scpc2", "password" : "swustscpc"}]})
        




