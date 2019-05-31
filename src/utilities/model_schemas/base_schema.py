"""Base schema module"""
from marshmallow import Schema
from src.utilities.exceptions.ValidationError import ValidationError
from src.messages.failure import error_msg


class BaseSchema(Schema):
    """Provides routine functions for child schemas"""

    def load_data(self, data):
        data, errors = self.load(data)
        if errors:
            raise ValidationError(error_msg['validation'], 400, errors)
        return data
