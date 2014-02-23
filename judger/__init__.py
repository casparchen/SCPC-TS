#coding=utf-8
import re,urllib,urllib2,cookielib,time
from application import db
from application.models import Submission
from judger.HDOJ import HDOJ
from sqlalchemy import or_, and_
import threading

def daemon(th, timeout, account):
        th.setDaemon(True)
        th.start()
        th.join(timeout)
        print "[Task #%s]: daemon killed or stoped." % th.submission.id
        account['used'] = False

class SCPC_Judger_Guard(object):
    """guard"""
    judgers = {}
    tasks = []
    MAX_JUDGE_TASK = 1

    def __init__(self, MAX_JUDGE_TASK):
        self.MAX_JUDGE_TASK = MAX_JUDGE_TASK

    def start(self):
        while True:
            print "[Main] current tasks:" + str(len(self.tasks))
            time.sleep(3)
            if len(self.tasks) == self.MAX_JUDGE_TASK: continue
            submission = self.request_new_submission_by_databse()
            if submission is not None:
                self.tasks.append(submission)
                self.judge(submission)
            

    def judge(self, task):
        spare_account = self.request_spare_judger(task.original_oj)
        spare_account['used'] = True
        print "select accout: ", spare_account
        j = self.judgers[task.original_oj]['oj'](spare_account)
        
        dm = threading.Thread(target=daemon,args=(j.judge(task), 12, spare_account))
        print "[Task #%s]: start daemon" % task.id
        dm.start()


    def request_spare_judger(self, oj):
        for x in self.judgers[oj]['account']:
            if 'used' not in x:
                return x
            elif x['used'] == False:
                return x
        return None

    def request_new_submission_by_databse(self):
        try:
            A = False
            B = False
            for x in self.judgers:
                if self.request_spare_judger(str(x)) != None:
                    A = or_(A, Submission.original_oj==str(x))
                    B = True
            if B != True: return None
            submission = Submission.query.filter(and_(Submission.judger_status==0, A)).first()
            if submission is not None:
                submission.judger_status = int(time.time())
                db.session.commit()
            return submission
        except Exception, e:
            return None
        

    def add_judger(self, judger):
        if judger['oj'].oj_name is not None and judger['oj'].oj_name != "":
            self.judgers[judger['oj'].oj_name] = judger

    def remove_task(self, task):
        print "[Task #%s]: Removed"
        if task in self.tasks:
            self.tasks.remove(task)

guard = SCPC_Judger_Guard(2)

guard.add_judger({"oj" : HDOJ, "account": [{"username" : "scpc1", "password" : "swustscpc"}, {"username" : "scpc2", "password" : "swustscpc"}]})
        




