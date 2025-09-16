import requests
from utils.logger import log_response


class APIClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, headers=None):
        """
        :param endpoint:
        :param headers:
        :return:
        """
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers if headers else self.headers
        )
        log_response(response)
        return response

    def post(self, endpoint, data, headers=None):
        """
        :param endpoint:
        :param data:
        :param headers:
        :return:
        """
        response = requests.post(
            f"{self.base_url}{endpoint}",
            json=data, headers=headers if headers else self.headers
        )
        log_response(response)
        return response

    def put(self, endpoint, data=None, headers=None):
        """
        Update endpoint
        :param endpoint:
        :param data:
        :param headers:
        :return:
        """
        response = requests.put(
            f"{self.base_url}{endpoint}",
            json=data, headers=headers if headers else self.headers
        )
        log_response(response)
        return response

    def delete(self, endpoint, headers=None):
        """
        Delete
        :param endpoint:
        :param headers:
        :return:
        """
        response = requests.delete(
            f"{self.base_url}{endpoint}",
            headers=headers if headers else self.headers
        )
        log_response(response)
        return response


