from flask import json
from src.models.user import User

BASE_URL = '/api/v1'
CHARSET = 'utf-8'


class TestUserOnboarding:
    def test_user_login_fails_with_unexisting_user(
            self,
            init_db,
            client,
    ):
        unexistingUser = {'email': 'okoro@gmail.com', 'password': 'password2'}
        response = client.post(
            f'{BASE_URL}/login', data=json.dumps(unexistingUser))
        parsed_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert parsed_response['message'] == 'User not found'
        assert parsed_response.get('token') is None

    def test_user_login_succeeds_with_saved_user(self, client, new_user):
        new_user.save()
        data = {'email': new_user.email, 'password': new_user.password}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        parsed_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert parsed_response['message'] == 'Login successful'
        assert parsed_response['token']
        assert parsed_response['data']['email'] == data['email']

    def test_user_login_fails_with_wrong_password(self, client, new_user):
        data = {'email': new_user.email, 'password': 'wrong-password'}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        parsed_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert parsed_response['message'] == 'Invalid login details'

    def test_user_login_fails_with_invalid_data(
            self,
            client,
    ):
        data = {'email': '54and&gmail.com', 'password': 'short'}
        response = client.post(f'{BASE_URL}/login', data=json.dumps(data))
        parsed_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert parsed_response['message'] == 'Field validation(s) faild'
        assert type(parsed_response['errors']) == dict
        assert parsed_response['errors']['email'] == [
            'Not a valid email address.'
        ]
        assert parsed_response['errors']['password'] == [
            'Password less than 6 chars'
        ]
