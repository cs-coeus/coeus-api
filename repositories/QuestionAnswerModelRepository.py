import os
from typing import Tuple, List, Any

from dotenv import dotenv_values

from repositories.DataRepository import DataRepository
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")


class QuestionAnswerModelRepository(DataRepository):
    def __init__(self):
        QuestionAnswerModelRepository.base_url = 'http://coeus.sit.kmutt.ac.th/api/model/qa'
        QuestionAnswerModelRepository.header = {
            "Authorization": f"Bearer {authentication_token}"}

    @staticmethod
    def get_prediction(original, keyword, questions):
        try:
            response = requests.post(
                f"{QuestionAnswerModelRepository.base_url}/predict",
                json={
                    "data": [
                        original,
                        keyword,
                        questions]},
                headers=QuestionAnswerModelRepository.header).json()
            result = response['result']
        except Exception as e:
            print(original, keyword, questions, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with summarizer model')
        return result

    @staticmethod
    def getData(input: Tuple[str, str, List[str]]) -> List[Any]:
        return QuestionAnswerModelRepository.get_prediction(
            input[0], input[1], input[2])
