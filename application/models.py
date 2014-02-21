from application import db

class User(db.Model):
    """entity for user"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)


    def __init__(self, username, password, email, scpc_oj_username, last_login_time):
        self.username = username
        self.password = password
        self.email = email
        self.scpc_oj_username = scpc_oj_username
        self.last_login_time = last_login_time
        
    def __repr__(self):
        return "<user %r>" % self.username

