#coding=utf-8

# database
SQLALCHEMY_DATABASE_URI = 'mysql://root:scpc@mrchenyi.com/SCPC_TS?charset=utf8'
SQLALCHEMY_ECHO = True
CONNECTION_ARGS = {'pool_recycle':3600}

# site name
SCPC_TS_SITE_NAME = 'SCPC Training System V2'

# WTForms
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Cache
CACHE_TYPE = 'simple'


