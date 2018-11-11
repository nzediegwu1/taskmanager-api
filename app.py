"""Module for handling application setup"""
import os

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from flask import Flask, Blueprint, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_restful import Api

from models.database import db
from views.users import LoginResource, UserResource
from index import Index
from config import configure_app
from utilities.exceptions.ValidationError import (ValidationError,
                                                  error_blueprint)

BASE_URL = '/api/v1'
load_dotenv()
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api.add_resource(Index, '/')
api.add_resource(UserResource, f'{BASE_URL}/users')
api.add_resource(LoginResource, f'{BASE_URL}/login')


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
