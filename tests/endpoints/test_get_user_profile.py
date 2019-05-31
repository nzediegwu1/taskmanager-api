from flask import json
from src.models.user import User
from src.messages.success import success_msg
from src.messages.failure import error_msg
from src.constants import BASE_URL, CHARSET, MIMETYPE
from tests.helpers import auth_header


class TestUserProfileGet:
    def test_get_user_profile_succeeds_with_valid_token_and_permission(
            self, init_db, client, new_user):
        new_user.save()
        headers = auth_header(new_user)
        response = client.get(f'{BASE_URL}/users/{new_user.id}',
                              headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert json_response['message'] == success_msg['profile']
        assert json_response['data']['name'] == new_user.name
        assert json_response['data']['email'] == new_user.email
        assert not json_response['data'].get('password')

    def test_authorizations(self, authorization_tests):
        authorization_tests(f'{BASE_URL}/users/1', 'get')

    def test_request_fails_with_invalid_id(self, client):
        user = User.find_one(email='nzediegwu1@gmail.com')
        headers = auth_header(user)
        response = client.get(f'{BASE_URL}/users/2rs', headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['message'] == error_msg['invalid_id']
        assert json_response['status'] == 'error'

    def test_request_fails_with_unexisting_user(self, client):
        user = User.find_one(email='nzediegwu1@gmail.com')
        headers = auth_header(user)
        response = client.get(f'{BASE_URL}/users/99', headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert json_response['message'] == error_msg['not_exists'].format(
            'User')
        assert json_response['status'] == 'error'

    def test_request_fails_when_not_permitted(self, client, second_user):
        second_user.save()
        headers = auth_header(second_user)
        response = client.get(f'{BASE_URL}/users/1', headers=headers)
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert json_response['message'] == error_msg['no_permission']
        assert json_response['status'] == 'error'
