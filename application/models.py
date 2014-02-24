#coding=utf-8
from application import db

class User(db.Model):
    """entity for user"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True, nullable = False)
    password = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(128), unique = True, nullable = False)
    scpc_oj_username = db.Column(db.String(128), unique = True)
    last_login_time = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    

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
        
    
class Problem(db.Model):
    """entity for problem"""
    id = db.Column(db.Integer, primary_key = True)
    owner_contest_id = db.Column(db.Integer)
    owner_road_id= db.Column(db.Integer)
    original_oj= db.Column(db.Text, nullable = False)
    original_oj_id= db.Column(db.Text, nullable = False)
    title= db.Column(db.Text, nullable = False)
    memory_limit= db.Column(db.Text)
    time_limit= db.Column(db.Text)
    description= db.Column(db.Text)
    input= db.Column(db.Text)
    output= db.Column(db.Text)
    sample_input= db.Column(db.Text)
    sample_output= db.Column(db.Text)
    hint= db.Column(db.Text)

    def __init__(self,owner_contest_id,owner_road_id,original_oj,original_oj_id,title,memory_limit,time_limit,description,input,output,sample_input,sample_output,hint):
        self.owner_contest_id = owner_contest_id
        self.owner_road_id = owner_road_id
        self.original_oj = original_oj
        self.title = title
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.description = description
        self.input = input
        self.output = output
        self.sample_input = sample_input
        self.sample_output = sample_output
        self.hint = hint
        self.original_oj_id = original_oj_id
        
        
        
class Contest(db.Model):
    """entity for contest"""
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text,nullable=False)
    description=db.Column(db.Text)
    end_time=db.Column(db.DateTime,nullable=False)
    end_time=db.Column(db.DateTime,nullable=False)
    problems=db.Column(db.Text)
    private=db.Column(db.Boolean,nullable=False)
    contestants=db.Column(db.Text)
    ranklist=db.Column(db.Text)
    
    def __init__(self,title,description,start_time,end_time,problems,private,contestance,ranklist):
        self.title=title
        self.description=description
        self.start_time=start_time
        self.end_time=end_time
        self.problems=problems
        self.private=private
        self.contestants=contestants
        self.ranklist=ranklist

	
	
class Submission(db.Model):
    """entity for submission"""
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('submissions', lazy='dynamic'))
    problem_id = db.Column(db.Integer,db.ForeignKey('problem.id'))
    problem = db.relationship('Problem', backref=db.backref('submissions', lazy='dynamic'), lazy='select')
    submit_time=db.Column(db.DateTime,nullable=False)
    compiler=db.Column(db.Text,nullable=False)
    result=db.Column(db.Text,nullable=False)
    memory_used=db.Column(db.Text)
    time_used=db.Column(db.Text)
    code=db.Column(db.Text,nullable=False)
    judger_status=db.Column(db.Integer, default=0)
    original_oj_submit_id=db.Column(db.Integer, default=0)
    original_oj= db.Column(db.Text, nullable = False)
    
    def __init__(self,user,problem,submit_time,compiler,code,result,memory_used,time_used,judger_status,original_oj):
        self.user=user
        self.problem=problem
        self.submit_time=submit_time
        self.compiler=compiler
        self.result=result
        self.memory_used=memory_used
        self.time_used=time_used
        self.code=code
        self.judger_status=judger_status
        self.original_oj = original_oj

		






