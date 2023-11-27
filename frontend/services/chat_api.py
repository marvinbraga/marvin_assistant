import json
from urllib.parse import urlparse

import requests


class ChatApi:
    def __init__(self, host, port):
        self._port = port
        self._host = host
        self._url = urlparse(f"http://{host}:{port}/api/chats").geturl()

    def get(self, user_id, conversation_id):
        response = requests.get(url=f"{self._url}/{user_id}/{conversation_id}")
        response.raise_for_status()
        return response.content

    def post(self, user_id, conversation_id, message):
        msg = {"message": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url=f"{self._url}/{user_id}/{conversation_id}",
            headers=headers,
            json=msg,
        )
        response.raise_for_status()
        return json.loads(response.content)
