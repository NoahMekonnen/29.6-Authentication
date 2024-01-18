from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__="users"

    username = db.Column(db.Text,primary_key=True)

    password = db.Column(db.Text,nullable=False)

    email = db.Column(db.Text,nullable=False)

    first_name = db.Column(db.Text,nullable=False)

    last_name = db.Column(db.Text,nullable=False)

class Feedback(db.Model):
    
    __tablename__="feedback"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.Text,nullable=False)

    content = db.Column(db.Text,nullable=False)

    username = db.Column(db.Text,db.ForeignKey('users.username'))

    user = db.relationship('User', backref = 'feedback' )