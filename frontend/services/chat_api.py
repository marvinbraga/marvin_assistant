import logging
from urllib.parse import urlparse

import aiohttp

logging.basicConfig(level=logging.INFO)
logging.info("Teste de log chat_api.")


class ChatApi:
    def __init__(self, host, port):
        self._port = port
        self._host = host
        self._url = urlparse(f"http://{host}:{port}/api/chats").geturl()

    async def get(self, user_id, conversation_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self._url}/{user_id}/{conversation_id}") as response:
                response.raise_for_status()
                return await response.json()

    async def post(self, user_id, conversation_id, message):
        msg = {"message": message}
        headers = {"Content-Type": "application/json"}
        logging.info(f"Enviando mensagem para {self._url}/{user_id}/{conversation_id}")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{self._url}/{user_id}/{conversation_id}",
                    headers=headers,
                    json=msg
            ) as response:
                response.raise_for_status()
                logging.info(f"Recebendo resposta: {response}")
                return await response.json()
