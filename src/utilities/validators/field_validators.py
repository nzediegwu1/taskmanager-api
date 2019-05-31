"""Marshmallow field validators"""
from marshmallow import ValidationError
from src.messages.failure import error_msg


def validate_password(password):
    """Validate password input"""
    if len(password.strip()) < 6:
        raise ValidationError(error_msg['invalid_password'])


def validate_name(name):
    """Validate name field"""
    if not name.replace(' ', '').isalpha():
        raise ValidationError(error_msg['invalid_name'])
