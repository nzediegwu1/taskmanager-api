"""Custom validation error handler"""
from flask import Blueprint, jsonify

error_blueprint = Blueprint('error', __name__)


class ValidationError(Exception):
    """Base Validation class for handling validation errors"""

    def __init__(self, message, code=400, errors=None):
        Exception.__init__(self)
        self.status_code = code
        self.errors = errors
        self.message = message

    def to_dict(self):
        response = {
            'status': 'error',
            'message': self.message,
            'errors': self.errors
        }
        return {key: value for key, value in response.items() if value}
