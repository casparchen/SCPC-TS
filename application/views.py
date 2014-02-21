#coding=utf-8
from flask import g, render_template, redirect, url_for
from application import app,lm
from application.forms import form_user_login
from application.models import User
from flask_login import login_user, logout_user, current_user, login_required
import json



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

        
    


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")





