"""Module for handling application setup"""
import os

from flask import Flask, Blueprint, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_restful import Resource, Api

from models.database import db
from views.users import LoginResource, UserResource
from config import configure_app
from utilities.response import success
from utilities.exceptions.ValidationError import (ValidationError,
                                                  error_blueprint)

load_dotenv()
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)


class HelloWorld(Resource):
    """Root endpoint"""

    def get(self):
        message = 'Welcome to Task-Manager api from flask!'
        return success(message)


api.add_resource(HelloWorld, '/')
api.add_resource(UserResource, '/users')
api.add_resource(LoginResource, '/login')


@error_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = error.to_dict()
    return jsonify(response), error.status_code


app.register_blueprint(error_blueprint)  # initialize error handler
configure_app(app)  # setup environment
db.init_app(app)  # connect sqlAlchemy to database

if __name__ == '__main__':
    app.run('localhost', 3000)
