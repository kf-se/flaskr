import os
import logging
import pickle

from flask import Flask
from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):

    # create the logger
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True 
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #from . import db
    db.init_app(app)

    with app.app_context():

        # load ML models.
        resource_path = os.path.join(app.root_path, 'resources/')
        nlp_model = pickle.load(open(resource_path + 'gnb_nlp_model.pickle', 'rb'))
        cv = pickle.load(open(resource_path + 'cv_nlp.pickle', 'rb'))
        g.nlp_model = nlp_model
        g.cv = cv

        from .models import User, Post, Likes
        db.create_all()
        
        from . import auth, blog, error_handler
        app.register_blueprint(auth.bp)
        app.register_blueprint(blog.bp)
        app.register_blueprint(error_handler.bp)
        app.add_url_rule('/', endpoint='index')

        return app