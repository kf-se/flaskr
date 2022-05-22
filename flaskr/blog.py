from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from .models import db, User, Post, Likes

import flaskr.nlp
import logging

bp = Blueprint('blog', __name__)


@bp.route('/<int:id>/like', methods=('POST',))
def like(id):
    post = get_post(id, False)

    if request.method == 'POST':
        print(request.form)
        value = request.form['value']
        post_likes = Likes.query.filter(
            Likes.post_id == id
        ).first()

        if post_likes == None:
            post_likes = Likes(post_id=post.id, likes=0, dislikes=0)
            db.session.add(post_likes)

        if value == 'like':
            post_likes.likes = post_likes.likes + 1
            
        else:
            post_likes.dislikes = post_likes.dislikes + 1
        
        db.session.commit()    
        
    return redirect(url_for('blog.index'))


@bp.route('/')
@bp.route('/index')
def index():
    current_app.logger.info(f"Loading start page")
    posts = Post.query.order_by(Post.created.desc()).all()

    current_app.logger.info(posts)
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    current_app.logger.info('serving create')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'Body is required.'
        
        if error is not None:
            flash(error)
        else:
            current_app.logger.info('Creating sentiment')
            try:
                sentiment = flaskr.nlp.sentiment(body)
            except:
                current_app.logger.error('')
                return redirect(url_for('blog.index'))
            current_app.logger.info('Sentiment created: {}'.format(sentiment))

            post = Post(title=title, body=body, sentiment=sentiment)
            user = User.query.filter(User.id == g.user.id).first()
            user.posts.append(post)
            
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = Post.query.filter(Post.id == id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.user_id != g.user.id:
        current_app.logger.debug(f"author id does not match with user")
        abort(403)
    
    return post


# Could refactor and combine post/create
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.add(post)
            db.session.commit()
            
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post.likes)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))



