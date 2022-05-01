from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import sys
import flaskr.nlp
import logging

bp = Blueprint('blog', __name__)


@bp.route('/<int:id>/like', methods=('POST',))
def like(id):
    post = get_post(id, False)
    db = get_db()

    if request.method == 'POST':
        print(request.form)
        value = request.form['value']
        
        if value == 'like':
            db.execute(
                'INSERT INTO likes (post_id, likes, dislikes) VALUES(?,?, 0)'
                'ON CONFLICT(post_id) DO UPDATE '
                'SET likes = likes + ? WHERE post_id = ?',
                (id, 1, 1, id)
            )
        else:
            db.execute(
                'INSERT INTO likes (post_id, likes, dislikes) VALUES(?,0,?)'
                'ON CONFLICT(post_id) DO UPDATE '
                'SET dislikes = dislikes + ? WHERE post_id = ?',
                (id, 1, 1, id)
            )
            
        db.commit()

    return redirect(url_for('blog.index'))


@bp.route('/')
def index():
    logging.info(f"loading start page")
    db = get_db()
    posts = db.execute(
        'SELECT post.id, user.id, user.username, post.title, post.body, post.created, post.author_id, post.sentiment,'
        ' IFNULL(likes.likes, "") as likes, IFNULL(likes.dislikes, "") as dislikes FROM user'
        ' INNER JOIN post ON post.author_id = user.id'
        ' LEFT JOIN likes ON likes.post_id = post.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
            sentiment = flaskr.nlp.sentiment(body)
            
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, sentiment)'
                ' VALUES (?,?,?,?)',
                (title, body, g.user['id'], sentiment)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        logging.info(f"author id does not match with user")
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
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))



