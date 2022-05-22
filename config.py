"""Flask configuration variables."""
import os

db_url = os.environ.get('DATABASE_URL')

class Config(object):
    SECRET_KEY = 'dev'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = db_url

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = db_url
    DEBUG = True