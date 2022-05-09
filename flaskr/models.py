from datetime import datetime
from . import db

class User(db.Model):
    """ DataModel for User profiles """

    __tablename__ = 'flaskr-users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    """ DataModel for blog Posts """

    __tablename__ = 'flaskr-posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(540), nullable=False)
    sentiment = db.Column(db.String(80), nullable=False)
    likes = db.relationship('Likes', backref='post', lazy=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class Likes(db.Model):
    """ DataModel for Likes/Dislikes associated with a Post """

    __tablename__ = 'flaskr-likes'
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Likes %r>' % self.post_id

