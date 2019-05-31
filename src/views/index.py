from flask_restful import Resource

from src.utilities.response import success


class Index(Resource):
    """Root endpoint"""

    def get(self):
        return success('Welcome to Task-Manager api from flask!')
