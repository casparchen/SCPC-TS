#coding=utf-8
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)



from application import views, models
