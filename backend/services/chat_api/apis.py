from urllib.parse import urlparse

import requests


class LlmApi:
    def __init__(self, host, port):
        self._port = port
        self._host = host
        self._url = urlparse(f"http://{host}:{port}/api/gpt").geturl()

    def post(self, conversation):
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=self._url, headers=headers, json=conversation)
        response.raise_for_status()
        return response.content
