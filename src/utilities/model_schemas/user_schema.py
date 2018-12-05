"""Module for user schema"""
from marshmallow import fields, validate, ValidationError
from .base_schema import BaseSchema
from ..validators.field_validators import validate_name, validate_password


class UserSchema(BaseSchema):
    """Marshmallow schema for user model"""
    name = fields.Str(required=True, validate=validate_name)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate_password)
