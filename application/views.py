#coding=utf-8
from flask import g,render_template
from application import app,lm
from application.forms import user_login_form
from application.models import User



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = user_login_form()
    if form.validate_on_submit():
        return "yes"
    return "no"

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")





