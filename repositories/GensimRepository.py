import os
from typing import Tuple, List, Any

from dotenv import dotenv_values

from repositories.DataRepository import DataRepository
import requests

is_production = os.environ.get('FLASK_ENV') == 'production'
authentication_token = os.environ.get('AUTHORIZATION_KEY')
config = dotenv_values(".env")


class GensimRepository(DataRepository):
    def __init__(self):
        GensimRepository.base_url = 'http://coeus.sit.kmutt.ac.th/api/model/gensim'
        GensimRepository.header = {
            "Authorization": f"Bearer {authentication_token}"}

    @staticmethod
    def get_word_embedding_of_word(word):
        try:
            response = requests.post(
                f"{GensimRepository.base_url}/predict/word_embedding",
                json={
                    "data": word},
                headers=GensimRepository.header).json()
            result = response['result']
        except Exception as e:
            print(word, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with gensim model')
        return result

    @staticmethod
    def getData(input: str) -> List[Any]:
        return GensimRepository.get_word_embedding_of_word(input)

    @staticmethod
    def get_wmd_between_sentence(sentence1, sentence2):
        try:
            response = requests.post(
                f"{GensimRepository.base_url}/predict/wmd",
                json={
                    "data": {
                        "word1": sentence1,
                        "word2": sentence2
                    }},
                headers=GensimRepository.header).json()
            result = response['result']
        except Exception as e:
            print(sentence1, sentence2, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with gensim model')
        return result
    
    @staticmethod
    def get_similarity_between_word(word1, word2):
        try:
            response = requests.post(
                f"{GensimRepository.base_url}/predict/similarity",
                json={
                    "data": {
                        "word1": word1,
                        "word2": word2
                    }},
                headers=GensimRepository.header).json()
            result = response['result']
        except Exception as e:
            print(word1, word2, flush=True)
            print(e, flush=True)
            raise Exception('Something went wrong with gensim model')
        return result
