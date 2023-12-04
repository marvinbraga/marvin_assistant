import os

from backend.services.whatsapp_api.utils.clients import WhatsAppClient, MessageProcessor, Logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class WhatsAppMessageHandler:
    def __init__(self, body):
        """
        Inicializa o manipulador de mensagens do WhatsApp.
        """
        self.body = body
        self.recipient_waid = os.environ["RECIPIENT_WAID"]
        self.whatsapp_client = WhatsAppClient()

    async def process_message(self) -> bool:
        """
        Processa a mensagem do WhatsApp de forma assíncrona.
        """
        if MessageProcessor.is_valid_whatsapp_message(self.body):
            wa_id = self.body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            name = self.body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
            Logger.show_info(f"wa_id = {wa_id}")
            Logger.show_info(f"name = {name}")

            message_body = self.body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            response = MessageProcessor.generate_response(message_body)
            data = WhatsAppClient.get_text_message_input(self.recipient_waid, response)

            await self.whatsapp_client.send_message(data)
            return True
        return False
