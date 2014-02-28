#coding=utf-8
from flask import g, render_template, redirect, url_for, request
from application import app,lm, cache, db
from application.forms import form_user_login
from application.models import User, News, Problem, Contest, Submission, Forum
from flask_login import login_user, logout_user, current_user, login_required
import json
import collections
import math
from datetime import datetime
    

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/user/<action>/', methods=['GET', 'POST'])
@app.route('/user/<action>', methods=['GET', 'POST'])
def login(action):
    if action == "login_status":
        if g.user is not None and g.user.is_authenticated():
            return json.dumps({"login_status" : True, "username" : g.user.username})
        else:
            return json.dumps({"login_status" : False})
    elif action == "login_form":
        form = form_user_login()
        return render_template('form_login.html', form = form)
    elif action == "login":
        form = form_user_login()
        if form.validate_on_submit():
            u = User.query.filter_by(username=form.username.data, password=form.password.data).first()
            if u is not None:
                login_user(u)
                return json.dumps({"result" : "ok", "username" : g.user.username})
        return json.dumps({"result" : "failed"})
    elif action == "logout":
        if g.user is not None and g.user.is_authenticated():
            logout_user()
            return json.dumps({"result" : "ok"})
        return json.dumps({"result" : "failed"})

    return redirect(url_for('index'))

@app.route('/news/<action>/<int:id>/')
@cache.cached(timeout=5)
def news(action, id):
    if action == "get":
        if type(id) is int:
            data = News.query.filter_by(id=id).first()
            return json.dumps(dict(
                id=data.id, 
                title=data.title, 
                content=data.content, 
                publish_time=str(data.publish_time))
            )

    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
        try:
            if len(request.form['code']) < 20:
                raise Exception("Code is too short. 20+ required.")
            if request.form['compiler'] != 'gcc' and request.form['compiler'] != 'g++' and request.form['compiler'] != 'java':
                raise Exception("Please select compiler.")
            user = g.user
            problem = int(request.form['problem_id'])
            problem = Problem.query.get(problem)
            if problem is None:
                raise Exception("Problem not found.")
            smt = Submission(user, problem, datetime.utcnow(), request.form['compiler'], request.form['code'], 'pending', "0K", "0MS", 0, problem.original_oj, problem.original_oj_id)
            db.session.add(smt)
            db.session.commit()
            return json.dumps({"result": "ok"})
        except Exception, e:
            return json.dumps({"result": str(e)})
    return json.dumps({"result": "Only support POST request."})


@app.route('/problems/')
@cache.cached(timeout=5)
def problems_no_page():
    return problems(0)

@app.route('/problems/<int:page>/')
@cache.cached(timeout=5)
def problems(page):
    if type(page) == int:
        page = 0 if page<1 else page-1
        data = Problem.query.limit(10).offset(page*10).all()
        objects_list = []
        for row in data:
            d = collections.OrderedDict()
            d['id'] = row.id
            d['title'] = row.title
            d['memory_limit'] = row.memory_limit
            d['time_limit'] = row.time_limit
            d['description'] = row.description
            d['input'] = row.input
            d['output'] = row.output
            d['sample_input'] = row.sample_input
            d['sample_output'] = row.sample_output
            d['hint'] = row.hint
            objects_list.append(d)
        return render_template('problems.html', 
            problems = objects_list,
            total_page = int(math.ceil(Problem.query.count()/10.0)),
            current_page = page + 1,
            site_name = app.config['SCPC_TS_SITE_NAME']
            )

    return redirect(url_for('index'))

@app.route('/problem/<int:id>/')
@cache.cached(timeout=5)
def problem(id):
    if type(id) == int:
        id = 1 if id < 1 else id
        p = Problem.query.get(id)
        return render_template('problem.html',
            site_name = app.config['SCPC_TS_SITE_NAME'],
            problem = p
            )


@app.route('/submissions/', defaults={'page': 1})
@app.route('/submissions/<int:page>')
@cache.cached(timeout=3)
def submissions_1(page):
    return submissions(page, None, None, None)

@app.route('/submissions/<int:page>:<user>:<int:problem>:<result>')
@cache.cached(timeout=3)
def submissions(page, user, problem, result):
    if type(page) == int:
        page = 0 if page<1 else page-1
        data = Submission.query.order_by(db.desc(Submission.id)).offset(page*10).limit(10).all()
        objects_list = []
        for row in data:
            d = collections.OrderedDict()
            d['id'] = row.id
            d['problem_title'] = row.problem.title
            d['username'] = row.user.username
            d['result'] = row.result
            d['memory_used'] = row.memory_used
            d['time_used'] = row.time_used
            d['compiler'] = row.compiler
            d['code'] = len(row.code)
            d['submit_time'] = row.submit_time
            objects_list.append(d)
        return render_template('submissions.html', 
            submissions = objects_list,
            total_page = int(math.ceil(Submission.query.count()/10.0)),
            current_page = page + 1,
            site_name = app.config['SCPC_TS_SITE_NAME']
            )
    return redirect(url_for('index'))

@app.route('/road/')
def road():
    return render_template('road.html', site_name = app.config['SCPC_TS_SITE_NAME'])

@app.route('/forum/', defaults={'page': 1})
@app.route('/forum/<int:page>')
@cache.cached(timeout=3)
def forum(page):
    if type(page) == int:
        page = 0 if page<1 else page-1
        data = Forum.query.filter(Forum.father_node==0,Forum.problem==None).order_by(db.desc(Forum.id)).offset(page*10).limit(10).all()
        objects_list = []
        for row in data:
            d = collections.OrderedDict()
            d['id'] = row.id
            d['title'] = row.title
            d['content'] = row.content
            d['last_update_time'] = row.last_update_time
            d['user'] = row.user.username
            d['last_reply'] = row.last_reply
            objects_list.append(d)
        return render_template('forum.html', 
            posts = objects_list,
            total_page = int(math.ceil(Forum.query.filter(Forum.father_node==0,Forum.problem==None).count()/10.0)),
            current_page = page + 1,
            site_name = app.config['SCPC_TS_SITE_NAME']
            )
    return redirect(url_for('index'))

@app.route('/forum/post/<int:id>/', defaults={'page': 1})
@app.route('/forum/post/<int:id>/<int:page>')
@cache.cached(timeout=5)
def post(id, page):
    if type(page) == int:
        page = 0 if page<1 else page-1
        if type(id) == int:
            id = 1 if id < 1 else id
            p = Forum.query.get(id)
            replys = Forum.query.filter(Forum.father_node == p.id).offset(page*10).limit(10).all()
            return render_template('post.html',
                site_name = app.config['SCPC_TS_SITE_NAME'],
                post = p,
                replys = replys,
                total_page = int(math.ceil(Forum.query.filter(Forum.father_node == p.id).count()/10.0)),
                current_page = page + 1
                )

@app.route('/contests/')
@app.route('/contests/<int:page>/')
@cache.cached(timeout=3)
def contests(page=0):
	if type(page)==int:
		page=0 if page<1 else page-1
		data=Contest.query.order_by(db.desc(Contest.id)).limit(10).offset(page*10).all()
		objects_list=[]
		for row in data:
			d=collections.OrderedDict()
			d['id']=row.id
			d['title']=row.title
			d['description']=row.description
			d['start_time']=row.start_time
			d['end_time']=row.end_time
			d['problems']=row.problems
			d['private']=row.private
			d['contestants']=row.contestants
			d['ranklist']=row.ranklist
			objects_list.append(d)
		return render_template("contests.html",
		    contests=objects_list,
		    total_page = int(math.ceil(Contest.query.count()/10.0)),
		    current_page = page + 1,
		    ctime=datetime.now(),
            site_name = app.config['SCPC_TS_SITE_NAME']
		)
		
	return redirect(url_for('index'))

@app.route('/contest/')
@app.route('/contest/<int:page>/')
def contest(page=1):
	if type(page)==int:
		if page<1:page=1
		row=Contest.query.get(page)
		problem_list=map(int,row.problems.split('|'))
		idlist=[]
		number_list=range(0,len(problem_list))
		for item in number_list:
			idlist.append(chr(ord('A') + item))
		problems=[]
		for item in problem_list:
			problems.append(Problem.query.get(item))
		totaltime=math.ceil((row.end_time-row.start_time).total_seconds()/60)
		havetime=math.ceil((row.end_time-datetime.now()).total_seconds()/60)
		if havetime<0:havetime=0
		elif havetime>totaltime:havetime=totaltime
		return render_template("contest.html",
             title=row.title,
             start_time=row.start_time,
             end_time=row.end_time,
             description=row.description,
             problems=problems,             #待优化
             idlist=idlist,
             number_list=number_list,
             totaltime=totaltime,
             havetime=havetime,
             site_name = app.config['SCPC_TS_SITE_NAME']
		     )
	return redirect(url_for('index'))
    
    
    
   
@app.route('/')
@app.route('/index')
@cache.cached(timeout=5)
def index():
    news_list = News.query.limit(8).all()
    return render_template("index.html", 
        news_list = news_list,
        site_name = app.config['SCPC_TS_SITE_NAME'])





