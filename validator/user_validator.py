import re

from utilities.response import Response

EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")


class Validator():
    res = Response()

    def validate_login(self, data):
        if data['email'] is None or not EMAIL_REGEX.match(data['email']):
            return self.res.error_resp('Invalid email', 400)
        elif data['password'] is None or len(data['password']) < 6:
            return self.res.error_resp('Password less than 6 chars', 400)

        return None

    def validate_user(self, data):
        if data['name'] is None or not data['name'].replace(' ', '').isalpha():
            return self.res.error_resp('Name must be all alpabets', 400)
        elif data['re_password'] != data['password']:
            return self.res.error_resp('Passwords do not match', 400)
        return None

    def validate_signup(self, data):
        login = self.validate_login(data) or self.validate_user(data)
        return login
