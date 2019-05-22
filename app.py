"""Module for handling application setup"""
from os import getenv

from flask_migrate import Migrate, upgrade
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_restful import Api

from src.views.index import Index
from src.views.users import LoginResource, UserResource

from src.models.database import db
from config import config
from src.utilities.exceptions.ValidationError import (ValidationError,
                                                      error_blueprint)

load_dotenv()
BASE_URL = '/api/v1'
config_name = getenv('FLASK_ENV') or 'production'


def initialize_errorhandlers(application):
    ''' Initialize error handlers '''
    application.register_blueprint(error_blueprint)


@error_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = error.to_dict()
    return jsonify(response), error.status_code


def initialize_api(app):
    api = Api(app)
    api.add_resource(Index, '/')
    api.add_resource(UserResource, f'{BASE_URL}/users')
    api.add_resource(LoginResource, f'{BASE_URL}/login')


def create_app(config=config[config_name]):
    """Return app object given config object."""
    app = Flask(__name__)

    app.config.from_object(config)

    jwt = JWTManager(app)

    # bind app to db
    db.init_app(app)

    # initialize error handlers
    initialize_errorhandlers(app)

    # initialize migration scripts
    migrate = Migrate(app, db)

    initialize_api(app)

    return app


app = create_app()
