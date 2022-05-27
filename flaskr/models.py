from datetime import datetime
from flaskr import db

class User(db.Model):
    """ DataModel for User profiles 
        username
        password
    """

    __tablename__ = 'flaskr_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='flaskr_users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    """ DataModel for blog Posts 
        author_id
        title
        body
        sentiment
    """

    __tablename__ = 'flaskr_posts'
    id = db.Column(db.Integer, primary_key=True)
    #author_id = db.Column(db.Integer, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(540), nullable=False)
    sentiment = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('flaskr_users.id'), nullable=False)

    likes = db.relationship('Likes', backref='flaskr_posts', lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Post %r>' % self.title


class Likes(db.Model):
    """ DataModel for Likes/Dislikes associated with a Post """

    __tablename__ = 'flaskr_likes'
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('flaskr_posts.id'), nullable=False, unique=True)

    def __repr__(self):
        return '<Likes %r>' % self.post_id

