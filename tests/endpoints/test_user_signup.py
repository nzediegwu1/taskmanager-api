from flask import json
from src.models.user import User
from src.messages.success import success_msg
from src.messages.failure import error_msg
from tests.mocks import mocks

BASE_URL = '/api/v1'
CHARSET = 'utf-8'


class TestUserOnboarding:
    def test_user_signup_succeeds_with_new_user(
            self,
            init_db,
            client,
    ):
        data = mocks['valid_user']
        response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert json_response['message'] == success_msg['signup']
        assert json_response['token']
        assert json_response['data']['email'] == data['email']

    def test_user_signup_fails_with_existing_user(self, client, new_user):
        new_user.save()
        data = {
            'email': new_user.email,
            'name': new_user.name,
            'password': new_user.password
        }
        response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert json_response['message'] == error_msg['exists'].format('User')
        assert json_response.get('token') is None

    def test_user_signup_fails_with_invalid_data(
            self,
            client,
    ):
        data = {
            'email': '54and&gmail.com',
            'password': 'short',
            'name': 'ana 4 &9'
        }
        response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['message'] == error_msg['validation']
        assert type(json_response['errors']) == dict
        assert json_response['errors']['email'] == [error_msg['invalid_email']]
        assert json_response['errors']['password'] == [
            error_msg['invalid_password']
        ]
        assert json_response['errors']['name'] == [error_msg['invalid_name']]
