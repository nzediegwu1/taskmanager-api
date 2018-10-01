"""Marshmallow field validators"""
from marshmallow import ValidationError


def validate_password(password):
    """Validate password input"""
    if len(password) < 6:
        raise ValidationError('Password less than 6 chars')


def validate_name(name):
    """Validate name field"""
    if not name.replace(' ', '').isalpha():
        raise ValidationError('Name must be all alpabets')
