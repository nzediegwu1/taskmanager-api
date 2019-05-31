from flask import json
from src.models.user import User
from src.messages.success import success_msg

BASE_URL = '/api/v1'
CHARSET = 'utf-8'


class TestLandingPage:
    def test_base_url_successful(
            self,
            client,
    ):
        response = client.get('/')
        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert json_response['message'] == success_msg['landing_page']
        assert json_response['status'] == 'success'
