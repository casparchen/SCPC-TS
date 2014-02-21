#coding=utf-8
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Flask instance
app = Flask(__name__)
app.config.from_object('config')

# Database instance
db = SQLAlchemy(app)

# Login Manager instance
lm = LoginManager()
lm.setup_app(app)

# Models
from application import models

# Views
from application import views





