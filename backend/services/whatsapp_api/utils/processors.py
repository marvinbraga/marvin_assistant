import os

from backend.services.whatsapp_api.utils.abstracts import AbstractMessageProcessor
from frontend.services.chat_api import ChatApi


class MessageProcessorReverse(AbstractMessageProcessor):
    @staticmethod
    def generate_response(response: str):
        """
        Gera uma resposta a partir do texto recebido.

        Este método converte o texto recebido para letras maiúsculas.

        :param response: String contendo o texto da resposta.
        :return: Texto da resposta em letras maiúsculas.
        """
        return response[::-1]


class MessageProcessorGpt(AbstractMessageProcessor):
    @staticmethod
    async def generate_response(response: str):
        """
        Envia uma mensagem para a API de chat e retorna a resposta.
        :param response: Mensagem a ser enviada.
        :return: Resposta da API de chat.
        """
        user_id, conversation_id = "marcus", "1"

        chat_api = ChatApi(host=os.environ["CHAT_HOST"], port=os.environ["CHAT_PORT"])
        resp = await chat_api.post(user_id=user_id, conversation_id=conversation_id, message=response)
        return MessageProcessorGpt._extract_response_message(resp)

    @staticmethod
    def _extract_response_message(response):
        conversation = response.get("conversation", {})
        messages = conversation.get("messages", [])
        msg = messages[-1].get("content") if messages else "No response received"
        return msg
