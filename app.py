import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    username = os.getenv('USERNAME', 'default_user')
    password = os.getenv('PASSWORD', 'default_pass')
    return jsonify({
        'username': username,
        'password': password
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
