from flask import Flask, request, jsonify

from db.users import users

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world, this is Simple-todo app from flask"


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    count = 0
    response = None
    for user in users:
        if user['username'] == username:
            count += 1
            if user['username'] == username and user['password'] == password:
                response = {'status': 'login successful!', 'data': user}
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
