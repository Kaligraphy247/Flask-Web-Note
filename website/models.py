from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date_time = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key always refrences a column of another database
    # this is a one to many relationship, i.e. one object with may children.
    # user is also the same as User. user is its representation in SQL
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    """Schema for User Model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # comment here ?
    # Note is capital coz, of the reference to Python here.
    notes = db.relationship('Note')

