"""Handles requests on user endpoints"""
from os import getenv
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, decode_token
from flask import json
from flask_restful import Resource, request

from src.models.user import User
from src.utilities.response import success
from src.utilities.model_schemas.user_schema import UserSchema
from src.utilities.exceptions.ValidationError import ValidationError

secret = getenv('JWT_SECRET_KEY')


def authentication(user, message):
    schema = UserSchema(exclude=['password'])
    res, code = success(message, schema.dump(user).data)
    # add token to response
    return {
        **res, 'token':
        create_access_token(user.id, expires_delta=timedelta(days=1))
    }, code


class LoginResource(Resource):
    def login(self, data):
        """Process user login

        Args:
            data(dict): user login details from schema
        Returns:
            tuple: success response with status code
        """
        user = User.find_one(email=data['email'])
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
        """Process user signup

        Args:
            data(dict): new user data from schema
        Returns:
            tuple: success response with status code
        """
        existing_user = User.find_one(email=data['email'])
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


def validate_id(func):
    def wrapper(*args, **kwargs):
        if not kwargs['user_id'].isdigit():
            raise ValidationError('id parameter should be a number')
        user = User.find_one(id=kwargs['user_id'])
        if not user:
            raise ValidationError('User does not exist', 404)
        return func(*args, user=user, user_id=kwargs['user_id'])

    return wrapper


def permission(func):
    def wrapper(*args, **kwargs):
        jwt = decode_token(request.headers['Authorization'][7:])
        if jwt['identity'] != int(kwargs['user_id']):
            raise ValidationError('You do not have permission to view', 403)
        return func(*args, **kwargs)

    return wrapper


class SingleUserResource(Resource):
    @validate_id
    @permission
    @jwt_required
    def get(self, **kwargs):
        """
        Endpoint for fetching profile of a logged in user
        """
        schema = UserSchema(exclude=['password'])
        return success('User profile', data=schema.dump(kwargs['user']).data)
