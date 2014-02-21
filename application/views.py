from application import app
from application import lm
from application.models import User
from flask import g
from application.forms import user_login_form

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = user_login_form()
    if form.validate_on_submit():
        return "yes"
    return "no"






