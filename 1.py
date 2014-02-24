from application import admin, models, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import flask_login
from flask import request
import urllib2,re
import json,sys
from flask import g, render_template, redirect, url_for, request
from application import app
reload(sys)
sys.setdefaultencoding('gb2312')
last_sub = []
problem_url = "http://acm.hdu.edu.cn/showproblem.php?pid=" + str(2902)
response = urllib2.urlopen(problem_url)
text  = response.read()
match = re.compile('<h1 style=\'color:#1A5CC8\'>(.*?)<\/h1>.*?Time Limit.*?\/(\d*).*?Problem Description.*?<div class=panel_content>(.*?)<\/div>.*?Input.*?<div class=panel_content>(.*?)<\/div>.*?Output.*?<div class=panel_content>(.*?)<\/div>.*?Sample Input.*?<div class=panel_content><pre>.*?>(.*?)<\/.*?<\/pre>.*?Sample Output.*?<pre>.*?>(.*?)<\/?div.*?<\/pre>', re.M | re.S)
last_sub = match.findall(text)
print last_sub
problem = {}
problem['title'] = last_sub[0][0]
problem['original_oj_id'] = last_sub[0][1]
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
print problem
