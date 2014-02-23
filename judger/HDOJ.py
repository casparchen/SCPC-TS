#coding=utf-8
from application import db
from application.models import Submission
from judger.judger_base import SCPC_Judger
import judger
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re 
import time

class HDOJ(SCPC_Judger):
    """acm.hdoj.edu.cn"""
    oj_name = "HDOJ"
    hdoj_username = ""
    hdoj_password = ""
    hdoj_last_submission_id = None
    account = None
    submission = None

    def __init__(self, account):
        SCPC_Judger.__init__(self)
        self.hdoj_username = account['username']
        self.hdoj_password = account['password']
        self.account = account

    def judge(self, submission):
        self.submission = submission
        return self

    def submit(self):
        login_url = "http://acm.hdu.edu.cn/userloginex.php?action=login";
        submit_url = "http://acm.hdu.edu.cn/submit.php?action=submit";

        #cookie处理器
        cookieJar = cookielib.LWPCookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cookieJar)  
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
        urllib2.install_opener(opener)  

        #打开登录主页面
        urllib2.urlopen(login_url)  

        #header  
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer' : '******'}  

        #Post数据 
        postData = {'username' : self.hdoj_username, 'userpass' : self.hdoj_password, 'login' : 'Sign In'}   
        postData = urllib.urlencode(postData)  

        # Login
        request = urllib2.Request(login_url, postData, headers)  
        response = urllib2.urlopen(request) 

        # Compiler 
        compiler = '1'
        if self.submission.compiler == 'gcc': compiler = '1'
        if self.submission.compiler == 'g++': compiler = '0'
        if self.submission.compiler == 'java': compiler = '5'

        #Post数据 
        postData = {'problemid' : self.submission.problem.original_oj_id, 'check' : '', 'language' : compiler, 'usercode' : self.submission.code}   
        postData = urllib.urlencode(postData)

        urllib2.urlopen(submit_url)  

        # Submit
        request = urllib2.Request(submit_url, postData, headers)  
        response = urllib2.urlopen(request)

    def request_last_submission(self):
        status_url = "http://acm.hdu.edu.cn/status.php?user=" + self.hdoj_username
        response = urllib2.urlopen(status_url)
        text  = response.read()
        match = re.compile('<input type=submit.*?<\/form>.*?height=22px>(.*?)<\/td><td>.*?<font.*?>(.*?)<\/font>.*?showproblem.*?<td>(.*?)<\/td><td>(.*?)<\/td>', re.M | re.S)
        last_sub = match.findall(text)
        return last_sub
        
    def run(self):
        try:
            self.hdoj_last_submission_id = self.request_last_submission()[0][0]
            self.submit()
            while True:
                current_sub = self.request_last_submission()
                if self.hdoj_last_submission_id == current_sub[0][0]:
                    time.sleep(3)
                    continue
                if current_sub[0][1] != 'Queuing' and current_sub[0][1] != 'Running' and current_sub[0][1] != 'Compiling':
                    Submission.query.filter_by(id=self.submission.id).update(dict(result=current_sub[0][1],judger_status=-1,memory_used=current_sub[0][3],time_used = current_sub[0][2],original_oj_submit_id = current_sub[0][0]))
                    judger.guard.remove_task(self.submission)
                    db.session.commit()
                    break
                Submission.query.filter_by(id=self.submission.id).update(dict(result=current_sub[0][1]))
                db.session.commit()
        except Exception, e:
            judger.guard.remove_task(self.submission)
            self.account['used'] = False
            print "something wrong here."










