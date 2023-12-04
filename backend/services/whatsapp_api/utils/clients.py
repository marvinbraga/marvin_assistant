import json
import logging
import os

import aiohttp
from dotenv import load_dotenv, find_dotenv

from backend.services.whatsapp_api.utils.abstracts import AbstractMessageProcessor
from backend.services.whatsapp_api.utils.config import configure_logging

load_dotenv(find_dotenv())
configure_logging()


class Logger:
    @staticmethod
    async def log_http_response(response):
        logging.info(f"Status: {response.status}")
        logging.info(f"Content-type: {response.headers.get('content-type')}")
        body = await response.text()
        logging.info(f"Body: {body}")

    @staticmethod
    def show_info(text):
        logging.info(f"[show info]: {text}")

    @staticmethod
    def log_error(message):
        logging.error(message)


class WhatsAppClient:
    def __init__(self):
        """
        Inicializa o cliente WhatsApp.

        Configura a URL base e os cabeçalhos para as solicitações HTTP.
        """
        version = os.environ["VERSION"]
        phone_id = os.environ["PHONE_NUMBER_ID"]
        token = os.environ["ACCESS_TOKEN"]
        self.base_url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    async def send_message(self, data):
        """
        Envia uma mensagem através da API do WhatsApp de forma assíncrona usando aiohttp.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, data=data, headers=self.headers, timeout=10) as response:
                    response.raise_for_status()
                    await Logger.log_http_response(response)
                    return await response.json()
            except aiohttp.ClientError as e:
                Logger.log_error(f"Request failed due to: {e}")
                return {"status": "error", "message": "Failed to send message"}

    @staticmethod
    def get_text_message_input(recipient, text):
        """
        Prepara os dados de uma mensagem de texto para envio via WhatsApp.
        """
        return json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        })
