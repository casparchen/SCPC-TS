#coding=utf-8
from application import db
from application.models import Submission
from judger.judger_base import SCPC_Judger
from sqlalchemy.exc import SQLAlchemyError
import judger
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re 
import time
import sys
from datetime import datetime
reload(sys)
sys.setdefaultencoding('gb2312')
problem_url = "http://poj.org/problem?id=" + str(1061)
response = urllib2.urlopen(problem_url)
text  = response.read()
match = re.compile("<div style='position: absolute.*?<div class=\"ptt\".*?>(青蛙的约会)<\/div>.*?Description.*?<div class=\"ptx\".*?>(.*?)<\/div>.*?Input.*?<div class=\"ptx\".*?>(.*?)<\/div>.*?Output.*?<div class=\"ptx\".*?>(.*?)<\/div>.*?Sample Input.*?<pre.*?>(.*?)<\/pre>.*?Sample Output.*?<pre.*?>(.*?)<\/pre>", re.M | re.S)
last_sub = match.findall(text)
print last_sub
"""
problem = {}
problem['title'] = last_sub[0][0]
problem['original_oj_id'] = hdoj_id
problem['time_limit'] = "1S"
problem['memory_limit'] = "65535K"
problem['description'] = last_sub[0][2]
problem['input'] = last_sub[0][3]
problem['output'] = last_sub[0][4]
problem['sample_input'] = last_sub[0][5]
problem['sample_output'] = last_sub[0][6]
problem['hint'] = ""
problem['sample_input'] = problem['sample_input'].replace('\r\n', '<br/>')
problem['sample_output'] = problem['sample_output'].replace('\r\n', '<br/>')
return self.render('admin/problem_form.html', problem=problem)
"""