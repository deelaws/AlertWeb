import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """description of class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to get string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ALERT_WEB_MAIL_SUBJECT_PREFIX = '[Rescue Alert]'
    ALERT_WEB_MAIL_SENDER = 'Rescue Alert <ralert@trailbuddi.com>'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ALERT_WEB_MAIL_SUBJECT_PREFIX = '[Rescue Alert]'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:qazwsx123@localhost/RescueApp'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'production database uri'
    DEBUG = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'testing database uri'

configuration = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
