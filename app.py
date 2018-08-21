import os

from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_restful import Resource, Api
from views.users import LoginResource, UserResource

load_dotenv()
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


class HelloWorld(Resource):
    def get(self):
        message = 'Hello world, this is Simple-todo app from flask!'
        return {'status': 'success', 'message': message}


api.add_resource(HelloWorld, '/')
api.add_resource(UserResource, '/users')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    # app.debug = True
    app.run('localhost', 3000)
