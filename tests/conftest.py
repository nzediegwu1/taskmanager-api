import pytest
from flask import json
from datetime import timedelta
from flask_jwt_extended import create_access_token
import time

from src.models.database import db
from src.models.user import User
from app import create_app
from config import config
from src.constants import BASE_URL, CHARSET, MIMETYPE
from tests.mocks import mocks
from src.messages.failure import error_msg


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
    return User(email='nzediegwu1@gmail.com',
                name='Anaeze Nsoffor',
                password='password1')


@pytest.fixture(scope='module')
def second_user(app):
    return User(email='ebere@gmail.com',
                name='Ebere Nsoffor',
                password='password1')


@pytest.fixture(scope='module')
def expired_token(app):
    token = create_access_token(1, expires_delta=timedelta(microseconds=1))
    time.sleep(1)
    return token


@pytest.fixture(scope='function')
def authorization_tests(client, expired_token):
    def func(url, method):
        headers = {'Content-Type': MIMETYPE, 'Accept': MIMETYPE}
        response = getattr(client, method)(url, headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert json_response['message'] == error_msg['no_token']

        headers = {**headers, 'Authorization': 'nasddfjnsjnfjsd'}
        response = getattr(client, method)(url, headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert json_response['message'] == error_msg['authorization']

        headers = {
            **headers, 'Authorization': 'Bearer {0}'.format(expired_token)
        }
        response = getattr(client, method)(url, headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert json_response['message'] == error_msg['session_expired']

    return func
