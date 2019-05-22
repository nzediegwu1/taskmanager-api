from flask import json
from src.models.user import User

BASE_URL = '/api/v1'
CHARSET = 'utf-8'


class TestLandingPage:
    def test_base_url_successful(
            self,
            client,
    ):
        response = client.get('/')
        parsed_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert parsed_response[
            'message'] == 'Welcome to Task-Manager api from flask!'
        assert parsed_response['status'] == 'success'
