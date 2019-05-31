from flask import json
from src.models.user import User
from src.messages.success import success_messages

BASE_URL = '/api/v1'
CHARSET = 'utf-8'

# test request succeeds with valid token and permission
# test request fails with invalid id
# test request fails with unexisting user
# test request fails with NO permission
# test request fails with invalid authorization: short token, no token, false token, and expired token

# write a base class test for authorization cases and inherit in child test classes
# create authorization tests fixture and invoke in test_authorization methods
# define decorator for authorization tests and use in classes


class TestUserOnboarding:
    pass
    # def test_get_user_profile_succeeds_with_valid_token_and_permission(
    #         self,
    #         init_db,
    #         client,
    # ):
    #     data = {
    #         'email': 'okoro@gmail.com',
    #         'name': 'Okoro Okafor',
    #         'password': 'password1'
    #     }
    #     response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
    #     parsed_response = json.loads(response.data.decode(CHARSET))
    #     assert response.status_code == 200
    #     assert parsed_response['message'] == success_messages['signup']
    #     assert parsed_response['token']
    #     assert parsed_response['data']['email'] == data['email']

    # def test_user_signup_fails_with_existing_user(self, client, new_user):
    #     new_user.save()
    #     data = {
    #         'email': new_user.email,
    #         'name': new_user.name,
    #         'password': new_user.password
    #     }
    #     response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
    #     parsed_response = json.loads(response.data.decode(CHARSET))
    #     assert response.status_code == 409
    #     assert parsed_response['message'] == 'User already exists'
    #     assert parsed_response.get('token') is None

    # def test_user_signup_fails_with_invalid_data(
    #         self,
    #         client,
    # ):
    #     data = {'email': '54and&gmail.com', 'password': 'short'}
    #     response = client.post(f'{BASE_URL}/users', data=json.dumps(data))
    #     parsed_response = json.loads(response.data.decode(CHARSET))
    #     assert response.status_code == 400
    #     assert parsed_response['message'] == 'Field validation(s) faild'
    #     assert type(parsed_response['errors']) == dict
    #     assert parsed_response['errors']['email'] == [
    #         'Not a valid email address.'
    #     ]
    #     assert parsed_response['errors']['password'] == [
    #         'Password less than 6 chars'
    #     ]
