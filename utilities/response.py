class Response():
    def error(self, message, code=400):
        return {'status': 'error', 'message': message}, code

    def success(self, message, data=None, code=200):
        response = {'status': 'success', 'data': data, 'message': message}
        data = data or response.pop('data')
        return response, code
