# from anyio import Event
# from sqlalchemy.ext.hybrid import hybrid_property
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from sqlalchemy.sql import func

# db = SQLAlchemy()


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     user_name = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(150))
#     recordings = db.relationship('Recording', back_populates='user')
#     canvastemplate = db.relationship('CanvasTemplate', back_populates='user')
#     notes = db.relationship('Note', back_populates='user')
    
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     title = db.Column(db.String(150),  nullable=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now, onupdate=func.now)
#     user = db.relationship('User', back_populates='notes')

# class Recording(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     data = db.Column(db.String(255))
#     date = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
#     user = db.relationship('User', back_populates='recordings')
    

# class CanvasTemplate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeingKey('user.id'))
#     template_data = db.Column(db.Text, nullable=False)
#     is_draft = db.Column(db.Boolean, default=True)
#     user = db.relationship('User', back_populates='canvastemplate')

from anyio import Event
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150))
    recordings = db.relationship('Recording', back_populates='user')
    canvastemplate = db.relationship('CanvasTemplate', back_populates='user')
    feedbackform = db.relationship('FeedbackForm', back_populates='user')
    notes = db.relationship('Note', back_populates='user')
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150),  nullable=True)
    data = db.Column(db.String(10000))
    style = db.Column(db.String(100))  
    ftype=db.Column(db.String(50))
    color=db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now, onupdate=func.now)
    user = db.relationship('User', back_populates='notes')

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    user = db.relationship('User', back_populates='recordings')
    

class CanvasTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    template_data = db.Column(db.Text, nullable=False)
    is_draft = db.Column(db.Boolean, default=True)
    user = db.relationship('User', back_populates='canvastemplate')


class FeedbackForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating= db.Column(db.String(12), nullable=False)
    answer= db.Column(db.Text, nullable=False)
    suggestion = db.Column(db.Text,nullable=False)
    name = db.Column(db.String(255),nullable=True)
    email= db.Column(db.String(255),nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = db.relationship('User', back_populates='feedbackform')
