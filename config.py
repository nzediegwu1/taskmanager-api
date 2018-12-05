"""Module for application config"""
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')


class Development(BaseConfig):
    DEBUG = True
    TESTING = True


class Test(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URI')


class Production(BaseConfig):
    pass


config = {
    'development': 'config.Development',
    'test': 'config.Test',
    'production': 'config.Production'
}
