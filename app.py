import os

from dotenv import dotenv_values
from flask import Flask, jsonify, request

from Client import Client

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")

app = Flask(__name__)
client = Client()


@app.route('/healthcheck')
def health_check():
    return 'OK'


@app.route('/semi-structured/predict', methods=['POST'])
def semi_structured_predict():
    if request.method == 'POST' and request.json is not None:
        if is_production:
            token = request.headers.get('Authorization').split(' ')[1]
            if token != authentication_token:
                return jsonify({"error": "Unauthorized request"}), 403
        topic = request.json['topic']
        if topic is not None:
            try:
                result = Client.generate_mind_map_from_semi_structure_text(topic)
                return jsonify({"result": result})
            except Exception as e:
                print(topic)
                print(e)
                return jsonify({"error": "Data format wrong"}), 400
    return jsonify({"error": "Data is invalid or not exist"}), 400


@app.route('/unstructured/predict', methods=['POST'])
def unstructured_predict():
    if request.method == 'POST' and request.json is not None:
        if is_production:
            token = request.headers.get('Authorization').split(' ')[1]
            if token != authentication_token:
                return jsonify({"error": "Unauthorized request"}), 403
        topic = request.json['topic']
        text = request.json['text']
        if topic is not None and text is not None:
            try:
                result = Client.generate_mind_map_from_unstructured_text(topic, text)
                return jsonify({"result": result})
            except Exception as e:
                print(topic)
                print(e)
                return jsonify({"error": "Data format wrong"}), 400
    return jsonify({"error": "Data is invalid or not exist"}), 400
