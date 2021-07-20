from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from nester.nest import create_group

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
     "admin": generate_password_hash("admin")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
def hello_world():
    return """
    Revolut REST Service for grouping list of dicts
    Use route: /create-nest 
    Content-Type: application/json
    body structure: {'arr': [{}, {}, {}], 'keys': [key1, key2, ...]}
    """


@app.route('/create-nest', methods=['POST'])
@auth.login_required
def create_nest():
    request_params = request.get_json()
    try:
        arr = request_params['arr']
        keys = request_params['keys']
    except KeyError as e:
        return f"Bad Request. Missing param: {e}", 400
    else:
        return create_group(arr, keys)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
