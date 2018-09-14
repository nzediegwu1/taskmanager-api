from flask_jwt_extended import create_access_token
from flask_restful import Resource, request

from models.users import users
from utilities.response import Response
from utilities.model_schemas.user_schema import UserSchema

response = Response()


class LoginResource(Resource):
    def login(self, data):
        visitor = None
        for user in users:
            if user['email'] == data['email']:
                visitor = user
                break
        if not visitor:
            return response.error('User not found', 404)
        elif data['password'] != visitor['password']:
            return response.error('Invalid login details', 401)
        schema = UserSchema(exclude=['password'])
        user, _ = schema.dump(visitor)
        res, code = response.success('Login successful', user)
        res['token'] = create_access_token(user['id'])
        return res, code

    def post(self):
        json_request = request.get_json(force=True)
        schema = UserSchema(only=['email', 'password'])
        data, errors = schema.load(json_request)
        if errors:
            return response.error(errors)
        return self.login(data)


class UserResource(Resource):
    def sign_up(self, data):
        for user in users:
            if user['email'] == data['email']:
                return response.error('User already exists', 409)
        data['id'] = len(users) + 1
        users.append(data)
        schema = UserSchema(exclude=['password'])
        new_user, _ = schema.dump(data)
        res, code = response.success('Signup successful', new_user, 201)
        res['token'] = create_access_token(new_user['id'])
        return res, code

    def post(self):
        json_data = request.get_json(force=True)
        schema = UserSchema()
        data, errors = schema.load(json_data)
        if errors:
            return response.error(errors)
        return self.sign_up(data)

    def get(self):
        schema = UserSchema(exclude=['password'], many=True)
        json_data, _ = schema.dump(users)
        return response.success('User list', json_data)
