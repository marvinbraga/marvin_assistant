import re
from abc import ABCMeta, abstractmethod


class AbstractMessageProcessor(metaclass=ABCMeta):
    @staticmethod
    def process_text_for_whatsapp(text):
        """
        Processa o texto recebido para o formato aceitável pelo WhatsApp.

        Este método remove caracteres especiais específicos e converte
        a formatação em negrito do markdown para o estilo do WhatsApp.

        :param text: String contendo o texto a ser processado.
        :return: Texto formatado para o estilo do WhatsApp.
        """
        text = re.sub(r"\&#8203;``&#8203;``【oaicite:0】``&#8203;``&#8203;", "", text).strip()
        whatsapp_style_text = re.sub(r"\*\*(.*?)\*\*", r"*\1*", text)
        return whatsapp_style_text

    @staticmethod
    @abstractmethod
    def generate_response(response):
        """
        Gera uma resposta a partir do texto recebido.

        Este método converte o texto recebido para letras maiúsculas.

        :param response: String contendo o texto da resposta.
        :return: Texto da resposta que será enviada ao Whatsapp.
        """
        pass

    @staticmethod
    def is_valid_whatsapp_message(body):
        """
        Verifica se a estrutura da mensagem recebida é válida para o WhatsApp.

        Este método checa se o corpo da mensagem contém os campos necessários
        para ser considerada uma mensagem válida do WhatsApp.

        :param body: Dicionário contendo o corpo da mensagem recebida.
        :return: Booleano indicando se a mensagem é válida ou não.
        """
        return (
                body.get("object") and
                body.get("entry") and
                body["entry"][0].get("changes") and
                body["entry"][0]["changes"][0].get("value") and
                body["entry"][0]["changes"][0]["value"].get("messages") and
                body["entry"][0]["changes"][0]["value"]["messages"][0]
        )
