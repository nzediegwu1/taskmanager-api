"""Handles requests on user endpoints"""
from os import getenv
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, decode_token
from flask import json
from flask_restful import Resource, request

from src.models.user import User
from src.utilities.response import success
from src.messages.failure import error_msg
from src.messages.success import success_msg
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
            raise ValidationError(error_msg['not_found'].format('User'), 404)
        elif user.password != data['password']:
            raise ValidationError(error_msg['wrong_login'], 401)

        return authentication(user, success_msg['login'])

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
            raise ValidationError(error_msg['exists'].format('User'), 409)

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


def permission(func):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            raise ValidationError(error_msg['no_token'], 401)
        jwt = decode_token(request.headers.get('Authorization')[7:])
        if jwt['identity'] != int(kwargs['id']):
            raise ValidationError(error_msg['no_permission'], 403)
        return func(*args, **kwargs)

    return wrapper


def validate_id(model, model_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not kwargs['id'].isdigit():
                raise ValidationError(error_msg['invalid_id'])
            instance = model.find_one(id=kwargs['id'])
            if not instance:
                raise ValidationError(
                    error_msg['not_exists'].format(model_name), 404)
            return func(*args, instance=instance, id=kwargs['id'])

        return wrapper

    return decorator


class SingleUserResource(Resource):
    @validate_id(User, 'User')
    @permission
    @jwt_required
    def get(self, **kwargs):
        """
        Endpoint for fetching profile of a logged in user
        """
        schema = UserSchema(exclude=['password'])
        return success(success_msg['profile'],
                       data=schema.dump(kwargs['instance']).data)
