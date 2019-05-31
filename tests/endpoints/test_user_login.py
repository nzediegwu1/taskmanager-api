from flask import json
from src.models.user import User
from src.messages.success import success_msg
from src.messages.failure import error_msg

BASE_URL = '/api/v1'
CHARSET = 'utf-8'


class TestUserOnboarding:
    def test_user_login_fails_with_unexisting_user(
            self,
            init_db,
            client,
    ):
        unexistingUser = {'email': 'okoro@gmail.com', 'password': 'password2'}
        response = client.post(f'{BASE_URL}/login',
                               data=json.dumps(unexistingUser))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert json_response['message'] == error_msg['not_found'].format(
            'User')
        assert json_response.get('token') is None

    def test_user_login_succeeds_with_saved_user(self, client, new_user):
        new_user.save()
        data = {'email': new_user.email, 'password': new_user.password}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert json_response['message'] == success_msg['login']
        assert json_response['token']
        assert json_response['data']['email'] == data['email']

    def test_user_login_fails_with_wrong_password(self, client, new_user):
        data = {'email': new_user.email, 'password': 'wrong-password'}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert json_response['message'] == error_msg['wrong_login']

    def test_user_login_fails_with_invalid_data(
            self,
            client,
    ):
        data = {'email': '54and&gmail.com', 'password': 'short'}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['message'] == error_msg['validation']
        assert type(json_response['errors']) == dict
        assert json_response['errors']['email'] == [error_msg['invalid_email']]
        assert json_response['errors']['password'] == [
            error_msg['invalid_password']
        ]
