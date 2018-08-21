class Response():
    def error_resp(self, message, code):
        return {'status': 'error', 'message': message}, code

    def succcess_resp(self, message, data, code):
        return {'status': 'success', 'data': data, 'message': message}, code
