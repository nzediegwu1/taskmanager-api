import pytest

from src.models.database import db
from src.models.user import User
from app import create_app
from config import config


@pytest.yield_fixture(scope='session')
def app():
    test_app = create_app(config['test'])

    ctx = test_app.app_context()
    ctx.push()
    yield test_app
    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='module')
def init_db(app):
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def new_user(app):
    return User(
        email='nzediegwu1@gmail.com',
        name='Anaeze Nsoffor',
        password='password1')
