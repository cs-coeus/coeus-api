import os

from dotenv import dotenv_values

from repositories.DataRepository import DataRepository
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")


class SpacyModelRepository(DataRepository):
    def __init__(self):
        SpacyModelRepository.base_url = 'http://coeus.sit.kmutt.ac.th/api/model/spacy'
        SpacyModelRepository.header = {
            "Authorization": f"Bearer {authentication_token}"}

    @staticmethod
    def get_sentence_count_prediction(data):
        try:
            response = requests.post(
                f"{SpacyModelRepository.base_url}/predict/sentences/count",
                json={
                    "data": data},
                headers=SpacyModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(data, flush=True)
            print(e, flush=True)
            raise Exception(
                'Something went wrong with spacy model sentence count')
        return result

    @staticmethod
    def get_sentences_prediction(data):
        try:
            response = requests.post(
                f"{SpacyModelRepository.base_url}/predict/sentences",
                json={
                    "data": data},
                headers=SpacyModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(data, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with spacy model sentence')
        return result

    @staticmethod
    def get_pos_prediction(data):
        try:
            response = requests.post(
                f"{SpacyModelRepository.base_url}/predict/pos",
                json={
                    "data": data},
                headers=SpacyModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(data, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with spacy model pos')
        return result

    @staticmethod
    def get_noun_chunks_with_entity_type_prediction(data):
        try:
            response = requests.post(
                f"{SpacyModelRepository.base_url}/predict/noun-chunks-with-entity-type",
                json={
                    "data": data},
                headers=SpacyModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(data, flush=True)
            print(e, flush=True)
            raise Exception(
                'Something went wrong with spacy model noun chunk with entity')
        return result

    @staticmethod
    def getData(input: str) -> None:
        return
