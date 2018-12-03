"""Custom validation error handler"""
from flask import Blueprint, jsonify

error_blueprint = Blueprint('error', __name__)


class ValidationError(Exception):
    """Base Validation class for handling validation errors"""

    def __init__(self, message, code=400, error=None):
        Exception.__init__(self)
        self.status_code = code
        self.error = error
        self.message = message

    def to_dict(self):
        error = {
            'status': 'error',
            'message': self.message,
            'errors': self.error
        }
        return {key: value for key, value in error.items() if value}
