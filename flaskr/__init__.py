import os
import logging
import pickle

from flask import Flask
from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):

    # create the logger
    #logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
    #                    format="%(asctime)s - %(levelname)s - %(message)s")
    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.info('Attached gunicorn logger...')
    
    # Get config based on environment
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'production':
        configuration = 'config.ProductionConfig'

    elif flask_env == 'development':
        configuration = 'config.DevelopmentConfig'  
    app.config.from_object(configuration)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #from . import db
    db.init_app(app)

    with app.app_context():

        # load ML models.
        app.logger.info('Loading ML models...')
        resource_path = os.path.join(app.root_path, 'resources/')
        nlp_model = pickle.load(open(resource_path + 'gnb_nlp_model.pickle', 'rb'))
        cv = pickle.load(open(resource_path + 'cv_nlp.pickle', 'rb'))
        g.nlp_model = nlp_model
        g.cv = cv

        from .models import User, Post, Likes
        app.logger.info('Creating database tables...')
        db.create_all()
        
        from . import auth, blog, error_handler
        app.logger.info('Registering blueprints...')
        app.register_blueprint(auth.bp)
        app.register_blueprint(blog.bp)
        app.register_blueprint(error_handler.bp)
        app.add_url_rule('/', endpoint='index')

        app.logger.info('App creation done...')
        return app