from application import admin, models, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import request
import urllib2,re
import json


class Add_HDOJ_Problem_View(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/request_id.html')

    @expose('/submit', methods=('GET','POST',))
    def submit(self):
        if request.method == 'POST':
            try:
                p = models.Problem(None, None, request.form['original_oj'], request.form['original_oj_id'], request.form['title'], request.form['memory_limit'], request.form['time_limit'], request.form['description'], request.form['input'], request.form['output'], request.form['sample_input'], request.form['sample_output'], request.form['hint'])
                db.session.add(p)
                db.session.commit()
                return json.dumps({"result" : "ok"})
            except Exception, e:
                db.session.rollback()
                return json.dumps({"result" : "Adding problem failed."})
        

    @expose('/request/<int:hdoj_id>')
    def request_1(self, hdoj_id):
        last_sub = []
        try:
            problem_url = "http://acm.hdu.edu.cn/showproblem.php?pid=" + str(hdoj_id)
            response = urllib2.urlopen(problem_url)
            text  = response.read()
            match = re.compile('<h1 style=\'color:#1A5CC8\'>(.*?)<\/h1>.*?Time Limit.*?\/(\d*).*?Problem Description.*?<div class=panel_content>(.*?)<\/div>.*?Input.*?<div class=panel_content>(.*?)<\/div>.*?Output.*?<div class=panel_content>(.*?)<\/div>.*?Sample Input.*?<div class=panel_content><pre>.*?>(.*?)<\/.*?<\/pre>.*?Sample Output.*?<pre>.*?>(.*?)<\/.*?<\/pre>', re.M | re.S)
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
            return self.render('admin/problem_form.html', problem=problem)
        except Exception, e:
            print e
            return ""
        return 'last_sub'
        

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Problem, db.session, category='Problem'))
admin.add_view(ModelView(models.News, db.session))
admin.add_view(ModelView(models.Contest, db.session))
admin.add_view(ModelView(models.Submission, db.session))
admin.add_view(Add_HDOJ_Problem_View(name='Add HDOJ Problem', category='Problem'))


        