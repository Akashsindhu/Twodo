from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#association table that relates User and Project
assocations = db.Table('assocations', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', secondary=assocations, backref=db.backref('contributors',lazy='dynamic'), lazy='dynamic')
    #todo = db.relationship('Todo', backref='owner', lazy='dynamic') #was post blog from notes

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    todos = db.relationship('Todo', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.name)  

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(256))
    complete = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

#Todo.__table__.drop(db.engine)
db.create_all()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))