import functools
import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

#from flaskr.db import get_db
from .models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is requiered.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            existing_user = User.query.filter(
                User.username == username
            ).first()
            if existing_user:
                error = f"User {username} is already registered."
                current_app.logger.error(error, exc_info=True)
            else:
                new_user = User(
                    username=username,
                    password=generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("auth.login"))

            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #db = get_db()
        error = None
        #user = db.execute(
        #    'SELECT * FROM user WHERE username = ?', (username,)
        #).fetchone()
        user = User.query.filter(
            User.username == username
        ).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash (error)
    
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #g.user = get_db().execute(
        #    'SELECT * FROM user WHERE id = ?', (user_id,)
        #).fetchone()
        g.user = User.query.filter(User.id == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view