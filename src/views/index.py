from flask_restful import Resource

from src.utilities.response import success
from src.messages.success import success_msg


class Index(Resource):
    """Root endpoint"""

    def get(self):
        return success(success_msg['landing_page'])
