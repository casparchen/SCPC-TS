from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class user_login_form(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()])
