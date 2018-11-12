"""Module for application config"""
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class Development(BaseConfig):
    DEBUG = True
    TESTING = True


class Test(BaseConfig):
    TESTING = True


class Production(BaseConfig):
    pass


config = {
    'development': 'config.Development',
    'test': 'config.Test',
    'production': 'config.Production'
}


def configure_app(app):
    environment = os.getenv('PYTHON_ENV')
    app.config.from_object(config[environment])
