import os
import re

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv
from flask_restful import Resource, Api, request

from db.users import users

load_dotenv()
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")


class HelloWorld(Resource):
    def get(self):
        return "Hello world, this is Simple-todo app from flask"


class Login(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        if email is None or not EMAIL_REGEX.match(email):
            message = 'Email not provided or invalid'
            return {'status': 'error', 'message': message}, 400
        elif password is None or len(password) < 6:
            message = 'Password not provided or invalid format'
            return {'status': 'error', 'message': message}, 400
        else:
            visitor = None
            for user in users:
                if user['email'] == email:
                    visitor = user
                    break
            if not visitor:
                message = 'User does not exist'
                return {'status': 'error', 'message': message}, 403
            elif password != visitor['password']:
                message = 'Invalid login details'
                return {'status': 'error', 'message': message}, 401
            else:
                current_user = {**visitor}
                del current_user['password']
                return {
                    'status': 'success',
                    'data': current_user,
                    'message': 'Login successful',
                    'token': create_access_token(current_user['id'])
                }


api.add_resource(HelloWorld, '/')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run('localhost', 3000)
