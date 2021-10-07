import os

from dotenv import dotenv_values

from repositories.DataRepository import DataRepository
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")


class SummarizerModelRepository(DataRepository):
    def __init__(self):
        SummarizerModelRepository.base_url = 'http://coeus.sit.kmutt.ac.th/api/model/summarizer'
        SummarizerModelRepository.header = {"Authorization": f"Bearer {authentication_token}"}

    @staticmethod
    def get_prediction(data):
        try:
            response = requests.post(f"{SummarizerModelRepository.base_url}/predict", json={"data": data}, headers=SummarizerModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(data, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with summarizer model')
        return result

    @staticmethod
    def getData(input: str) -> str:
        return SummarizerModelRepository.get_prediction(input)
