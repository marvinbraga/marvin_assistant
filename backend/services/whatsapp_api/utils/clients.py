import json
import logging
import os

import httpx
from backend.services.whatsapp_api.utils.abstracts import AbstractMessageProcessor
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Logger:
    @staticmethod
    def log_http_response(response):
        logging.info(f"Status: {response.status_code}")
        logging.info(f"Content-type: {response.headers.get('content-type')}")
        logging.info(f"Body: {response.text}")

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
        Envia uma mensagem através da API do WhatsApp de forma assíncrona.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, data=data, headers=self.headers, timeout=10)
                response.raise_for_status()
                Logger.log_http_response(response)
                return response.json()
            except httpx.TimeoutException:
                Logger.log_error("Timeout occurred while sending message")
                return {"status": "error", "message": "Request timed out"}
            except httpx.RequestError as e:
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


class MessageProcessor(AbstractMessageProcessor):
    @staticmethod
    def generate_response(response):
        """
        Gera uma resposta a partir do texto recebido.

        Este método converte o texto recebido para letras maiúsculas.

        :param response: String contendo o texto da resposta.
        :return: Texto da resposta em letras maiúsculas.
        """
        return response.upper()
