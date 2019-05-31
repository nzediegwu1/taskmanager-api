from flask_jwt_extended import create_access_token
from src.constants import MIMETYPE


def auth_header(user):
    token = create_access_token(user.id)
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }
