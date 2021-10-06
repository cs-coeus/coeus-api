import os
from dotenv import dotenv_values
from flask import Flask, jsonify, request
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")

app = Flask(__name__)


@app.route('/healthcheck')
def health_check():
    return 'OK'

@app.route('/healthcheck/model')
def health_check_model():
    response = requests.get("http://127.0.0.1:80/api/model/summarizer/healthcheck")
    return response

