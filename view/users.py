from flask_jwt_extended import create_access_token
from flask_restful import Resource, request

from db.users import users
from utilities.response import Response
from validator.user_validator import Validator


class Login(Resource):
    res = Response()
    val = Validator()

    def login(self, data):
        visitor = None
        for user in users:
            if user['email'] == data['email']:
                visitor = {**user}
                break
        if not visitor:
            return self.res.error_resp('User does not exist', 403)
        elif data['password'] != visitor['password']:
            return self.res.error_resp('Invalid login details', 401)
        del visitor['password']
        return {
            'status': 'success',
            'data': visitor,
            'message': 'Login successful',
            'token': create_access_token(visitor['id'])
        }

    def post(self):
        req = request.form
        data = {'email': req.get('email'), 'password': req.get('password')}
        login = self.val.validate_login(data) or self.login(data)
        return login


class Signup(Resource):
    res = Response()
    val = Validator()

    def sign_up(self, data):
        for user in users:
            if user['email'] == data['email']:
                return self.res.error_resp('User already exists', 409)
        data['id'] = len(users) + 1
        del data['re_password']
        users.append(data)
        new_user = {**data}
        del new_user['password']
        return {
            'status': 'success',
            'data': new_user,
            'message': 'Signup successful',
            'token': create_access_token(new_user['id'])
        }, 201

    def post(self):
        req = request.form
        data = {
            'name': req.get('name'),
            'email': req.get('email'),
            'password': req.get('password'),
            're_password': req.get('re_password')
        }
        register = self.val.validate_signup(data) or self.sign_up(data)
        return register

    def get(self):
        return {'status': 'success', 'data': users, 'message': 'User list'}
