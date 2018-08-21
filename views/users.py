from flask_jwt_extended import create_access_token
from flask_restful import Resource, request

from models.users import users
from utilities.response import Response
from utilities.model_schemas.user_schema import UserSchema


class LoginResource(Resource):
    res = Response()

    def login(self, data):
        visitor = None
        for user in users:
            if user['email'] == data['email']:
                visitor = user
                break
        if not visitor:
            return self.res.error_resp('User does not exist', 403)
        elif data['password'] != visitor['password']:
            return self.res.error_resp('Invalid login details', 401)
        schema = UserSchema(exclude=['password'])
        user, _ = schema.dump(visitor)
        res, code = self.res.succcess_resp('Login successful', user, 200)
        res['token'] = create_access_token(user['id'])
        return res, code

    def post(self):
        json_request = request.get_json(force=True)
        schema = UserSchema(only=['email', 'password'])
        data, errors = schema.load(json_request)
        if errors:
            return self.res.error_resp(errors, 400)
        return self.login(data)


class UserResource(Resource):
    res = Response()

    def sign_up(self, data):
        for user in users:
            if user['email'] == data['email']:
                return self.res.error_resp('User already exists', 409)
        data['id'] = len(users) + 1
        users.append(data)
        schema = UserSchema(exclude=['password'])
        new_user, _ = schema.dump(data)
        res, code = self.res.succcess_resp('Signup successful', new_user, 201)
        res['token'] = create_access_token(new_user['id'])
        return res, code

    def post(self):
        json_data = request.get_json(force=True)
        schema = UserSchema()
        data, errors = schema.load(json_data)
        if errors:
            return self.res.error_resp(errors, 400)
        return self.sign_up(data)

    def get(self):
        schema = UserSchema(exclude=['password'], many=True)
        json_data, _ = schema.dump(users)
        return {'status': 'success', 'data': json_data, 'message': 'User list'}
