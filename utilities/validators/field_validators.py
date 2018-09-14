from marshmallow import ValidationError


def validate_password(password):
    if len(password) < 6:
        raise ValidationError('Password less than 6 chars')


def validate_name(name):
    if not name.replace(' ', '').isalpha():
        raise ValidationError('Name must be all alpabets')
