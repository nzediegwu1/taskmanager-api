"""Base schema module"""
from marshmallow import Schema
from ..exceptions.ValidationError import ValidationError


class BaseSchema(Schema):
    """Provides routine functions for child schemas"""

    def load_data(self, data):
        data, errors = self.load(data)
        if errors:
            raise ValidationError('Field validation(s) faild', 400, errors)
        return data
