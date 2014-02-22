#coding=utf-8
import re,urllib,urllib2,cookielib
import time
from application import db
from application.models import Submission

class SCPC_Judger_Guard(object):
    """guard"""
    def start(self):
        pass
    def request_new_submission_by_databse(self):
        submission = Submission.query.filter_by(judger_status=0).first()
        submission.judger_status = int(time.time())
        db.session.commit()
        return submission
    def 

guard = SCPC_Judger_Guard()

        




