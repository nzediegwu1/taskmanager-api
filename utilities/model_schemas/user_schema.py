from marshmallow import fields, Schema, validate, ValidationError

from ..validators.field_validators import validate_name, validate_password


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True, validate=validate_name)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate_password)
