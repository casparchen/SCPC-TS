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
import json
from datetime import datetime
login_url = "http://acm.swust.edu.cn:8080/"
login_action = "http://acm.swust.edu.cn:8080/user/ajaxlogin/"
print login_action
#cookie处理器
cookieJar = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cookieJar)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  

#打开登录主页面
text = urllib2.urlopen(login_url).read()
match = re.compile('action=\"\/user\/login/\".*?csrfmiddlewaretoken.*?value.*?\'(.*?)\'', re.M | re.S)
token = match.findall(text)[0]
print token

#header  
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer' : '******'}  

#Post数据 
postData = {'username' : 'chenyi', 'password' : '19890113', 'csrfmiddlewaretoken' : token}   
postData = urllib.urlencode(postData)  

# Login
request = urllib2.Request(login_action, postData, headers)  
response = urllib2.urlopen(request) 
text= response.read()
print text
email_url = "http://acm.swust.edu.cn:8080/user/juserinfo/?operation=profile"
request = urllib2.Request(email_url, None, headers)
response = urllib2.urlopen(request)
text = response.read() 
print json.loads(text)['email']