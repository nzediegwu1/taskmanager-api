from marshmallow import fields, Schema, validates, ValidationError


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('password')
    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password less than 6 chars')

    @validates('name')
    def validate_name(self, name):
        if not name.replace(' ', '').isalpha():
            raise ValidationError('Name must be all alpabets')
