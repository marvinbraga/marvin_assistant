import os

from dotenv import load_dotenv, find_dotenv

from backend.services.whatsapp_api.utils.clients import WhatsAppClient, Logger
from backend.services.whatsapp_api.utils.processors import MessageProcessorGpt, MessageProcessorReverse

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
        processor = MessageProcessorGpt  # MessageProcessorReverse
        if processor.is_valid_whatsapp_message(self.body):
            wa_id = self.body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            name = self.body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
            Logger.show_info(f"wa_id = {wa_id}")
            Logger.show_info(f"name = {name}")

            message_body = self.body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            response = await processor.generate_response(message_body)
            Logger.show_info(f"response = {response}")
            data = WhatsAppClient.get_text_message_input(self.recipient_waid, response)

            await self.whatsapp_client.send_message(data)
            return True
        return False
