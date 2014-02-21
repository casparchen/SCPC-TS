from application import db

class User(db.Model):
    """entity for user"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True, nullable = False)
    password = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(128), unique = True, nullable = False)
    scpc_oj_username = db.Column(db.String(128), unique = True)
    last_login_time = db.Column(db.DateTime)
    

    def __init__(self, username, password, email, scpc_oj_username, last_login_time):
        self.username = username
        self.password = password
        self.email = email
        self.scpc_oj_username = scpc_oj_username
        self.last_login_time = last_login_time
        
    def __repr__(self):
        return "<user %r>" % self.username

class News(db.Model):
    """entity for news"""
    id = db.Column(db.Integer, primary_key = True)
    publish_time = db.Column(db.DateTime, nullable = False)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text)


    def __init__(self, publish_time, title, content):
        self.publish_time = publish_time
        self.title = title
        self.content = content

    def __repr__(self):
        return "<news %r>" % self.title
        
    
        









