"""Module for handling application setup"""
import os

from flask_migrate import Migrate, upgrade
from flask import Flask, Blueprint, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_restful import Api

from index import Index
from views.users import LoginResource, UserResource

from models.database import db
from config import configure_app
from utilities.exceptions.ValidationError import (ValidationError,
                                                  error_blueprint)

BASE_URL = '/api/v1'
load_dotenv()
app = Flask(__name__)
api = Api(error_blueprint)

# @error_blueprint.app_errorhandler(ValidationError)
# def handle_exception(error):
#     """Error handler called when a ValidationError Exception is raised"""

#     response = error.to_dict()
#     return jsonify(response), error.status_code

# app.register_blueprint(error_blueprint)  # initialize error handler

# handle_exceptions = app.handle_exception
# handle_user_exceptions = app.handle_user_exception
# app.handle_exception = handle_exceptions
# app.handle_user_exception = handle_user_exceptions


@app.errorhandler(ValidationError)
@error_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = error.to_dict()
    return jsonify(response), error.status_code


app.register_blueprint(error_blueprint)  # initialize error handler

jwt = JWTManager(app)

migrate = Migrate(app, db)

api.add_resource(Index, '/')
api.add_resource(UserResource, f'{BASE_URL}/users')
api.add_resource(LoginResource, f'{BASE_URL}/login')

configure_app(app)  # setup environment
db.init_app(app)  # connect sqlAlchemy to database

if __name__ == '__main__':
    app.run('localhost', 3000)
