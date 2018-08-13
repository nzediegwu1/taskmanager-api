class Response():
    def error_resp(self, message, code):
        return {'status': 'error', 'message': message}, code
