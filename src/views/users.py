"""Handles requests on user endpoints"""
from flask_jwt_extended import create_access_token
from flask_restful import Resource, request

from ..models.user import User
from ..utilities.response import success
from ..utilities.model_schemas.user_schema import UserSchema
from ..utilities.exceptions.ValidationError import ValidationError


def authentication(user, message):
    schema = UserSchema(exclude=['password'])
    res, code = success(message, schema.dump(user).data)
    # add token to response
    res['token'] = create_access_token(user.id)
    return res, code


class LoginResource(Resource):
    def login(self, data):
        """
        Process user login

        Parameters:
            data(dict): user login details from schema
        Returns:
            Response(tuple): success response with status code
        """
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            raise ValidationError('User not found', 404)
        elif user.password != data['password']:
            raise ValidationError('Invalid login details', 401)

        return authentication(user, 'Login successful')

    def post(self):
        """
        Endpoint to handle user login
        """
        json_request = request.get_json(force=True)
        schema = UserSchema(only=['email', 'password'])
        data = schema.load_data(json_request)
        return self.login(data)


class UserResource(Resource):
    """Resource to handle users transactions"""

    def sign_up(self, data):
        """
        Method to process user signup

        Parameters:
            data(dict): new user data from schema
        Returns:
            Response(tuple): success response with status code
        """
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise ValidationError('User already exists', 409)

        new_user = User(**data)
        new_user.save()

        return authentication(new_user, 'Signup successful')

    def post(self):
        """
        Endpoint to handle user signup
        """
        json_data = request.get_json(force=True)
        schema = UserSchema()
        data = schema.load_data(json_data)
        return self.sign_up(data)

    def get(self):
        """
        Endpoint to retrieve registered users
        """
        schema = UserSchema(exclude=['password'], many=True)
        users = User.query.all()
        return success('User list', schema.dump(users).data)
