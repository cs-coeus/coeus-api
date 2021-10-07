import os
from typing import Tuple, List, Any

from dotenv import dotenv_values

from repositories.DataRepository import DataRepository
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")


class ClusteringModelRepository(DataRepository):
    def __init__(self):
        ClusteringModelRepository.base_url = 'http://coeus.sit.kmutt.ac.th/api/model/clustering'
        ClusteringModelRepository.header = {"Authorization": f"Bearer {authentication_token}"}

    @staticmethod
    def get_prediction(X, total_sent, proximity_matrix):
        try:
            response = requests.post(f"{ClusteringModelRepository.base_url}/predict", json={"data": [X, total_sent, proximity_matrix]}, headers=ClusteringModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(X, total_sent, proximity_matrix, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with summarizer model')
        return result

    @staticmethod
    def getData(input: Tuple[List[str], int, List[List[int]]]) -> List[Any]:
        return ClusteringModelRepository.get_prediction(input[0], input[1], input[2])
