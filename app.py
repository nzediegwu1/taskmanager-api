from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv
import os
import re

from db.users import users

load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")


@app.route('/')
def hello():
    return "Hello world, this is Simple-todo app from flask"


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or not EMAIL_REGEX.match(email):
        message = 'email not provided or invalid'
        return jsonify({'status': 'error', 'message': message}), 400
    elif password is None or len(password) < 6:
        message = 'password not provided or invalid'
        return jsonify({'status': 'error', 'message': message}), 400
    else:
        count = 0
        response = None
        for user in users:
            if user['email'] == email:
                count += 1
                if user['email'] == email and user['password'] == password:
                    response = {
                        'status': 'success',
                        'data': user,
                        'message': 'login successful',
                        'token': create_access_token(user['id'])
                    }
                    break
        if count:
            if response:
                return jsonify(response)
            else:
                data = {'status': 'error', 'message': 'invalid login details'}
                return jsonify(data), 401
        data = {'status': 'error', 'message': 'user does not exist'}
        return jsonify(data), 403


if __name__ == '__main__':
    app.debug = True
    app.run('localhost', 3000)
