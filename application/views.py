#coding=utf-8
from flask import g, render_template, redirect, url_for
from application import app,lm
from application.forms import form_user_login
from application.models import User, News, Problem, Contest, Submission
from flask_login import login_user, logout_user, current_user, login_required
import json
import collections



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user



@app.route('/user/<action>', methods = ['GET', 'POST'])
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
        print form.username.data,form.password.data
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

@app.route('/news/<action>/<int:id>')
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

@app.route('/problems/')
def problems_no_begin():
    return problems(0)
@app.route('/problems/<int:begin>')
def problems(begin):
    if type(begin) == int:
        data = Problem.query.limit(3).offset(begin).all()
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
        return render_template('problems.html', problems = objects_list)

    return redirect(url_for('index'))


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    news_list = News.query.limit(8).all()
    return render_template("index.html", news_list = news_list)





