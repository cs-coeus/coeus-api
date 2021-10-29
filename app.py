import os
from datetime import datetime, timedelta

from dotenv import dotenv_values
from flask import Flask, jsonify, request
from flask_cors import CORS

from Client import Client
from utils.FileParser import FileParser

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")

app = Flask(__name__)
client = Client()
CORS(app)

caches = {}
CACHE_TIMEOUT_IN_MINUTE = 30

file_parser = FileParser()

@app.route('/healthcheck')
def health_check():
    return 'OK'


@app.route('/predict/semi-structured', methods=['POST'])
def semi_structured_predict():
    if request.method == 'POST' and request.json is not None:
        if is_production:
            token = request.headers.get('Authorization').split(' ')[1]
            if token != authentication_token:
                return jsonify({"error": "Unauthorized request"}), 403
        wiki_path = request.json['wiki_path']
        if wiki_path is not None:
            if wiki_path in caches.keys():
              if datetime.now() < caches[wiki_path]['expire_time']:
                return jsonify({"result": caches[wiki_path]['result']})
            try:
                result = Client.generate_mind_map_from_semi_structure_text(
                    wiki_path)
                caches[wiki_path] = {
                  'expire_time': datetime.now() + timedelta(minutes=CACHE_TIMEOUT_IN_MINUTE),
                  'result': result
                }
                return jsonify({"result": result})
            except Exception as e:
                print(wiki_path, flush=True)
                print(e, flush=True)
                return jsonify({"error": "Data format wrong"}), 400
    return jsonify({"error": "Data is invalid or not exist"}), 400

@app.route('/predict/unstructured/text', methods=['POST'])
def unstructured_text_predict():
    if request.method == 'POST' and request.json is not None:
        if is_production:
            token = request.headers.get('Authorization').split(' ')[1]
            if token != authentication_token:
                return jsonify({"error": "Unauthorized request"}), 403
        topic = request.json['topic']
        text = request.json['text']
        if topic is not None and text is not None:
            try:
                result = Client.generate_mind_map_from_unstructured_text(
                    topic, text)
                return jsonify({"result": result})
            except Exception as e:
                print(topic, flush=True)
                print(text, flush=True)
                print(e, flush=True)
                return jsonify({"error": "Data format wrong"}), 400
    return jsonify({"error": "Data is invalid or not exist"}), 400

@app.route('/predict/unstructured/file', methods=['POST'])
def unstructured_file_predict():
    if request.method == 'POST':
        if is_production:
            token = request.headers.get('Authorization').split(' ')[1]
            if token != authentication_token:
                return jsonify({"error": "Unauthorized request"}), 403
        topic = request.form['topic']
        input_file = request.files['file']
        if input_file.filename == '':
            return jsonify({"error": "file not found"}), 400
        else:
            text = file_parser.parse_file(input_file)
        if topic is not None and text is not None:
            try:
                result = Client.generate_mind_map_from_unstructured_text(
                    topic, text)
                return jsonify({"result": result})
            except Exception as e:
                print(topic, flush=True)
                print(text, flush=True)
                print(e, flush=True)
                return jsonify({"error": "Data format wrong"}), 400
    return jsonify({"error": "Data is invalid or not exist"}), 400
