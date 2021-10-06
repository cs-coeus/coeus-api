import os
from dotenv import dotenv_values
from flask import Flask, jsonify, request


is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")

app = Flask(__name__)


@app.route('/healthcheck')
def health_check():
    return 'OK'

