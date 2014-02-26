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

datetime.utcnow(8)

login_url = "http://poj.org/login";
#cookie处理器
cookieJar = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cookieJar)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
 

#header  
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer' : '******'}  


status_url = "http://poj.org/status?user_id=" + '20081816'
request = urllib2.Request(status_url, None, headers)  
response = urllib2.urlopen(request)
text  = response.read()
print text
match = re.compile('<input type=submit.*?<\/form>.*?height=22px>(.*?)<\/td><td>.*?<font.*?>(.*?)<\/font>.*?showproblem.*?<td>(.*?)<\/td><td>(.*?)<\/td>', re.M | re.S)
last_sub = match.findall(text)
