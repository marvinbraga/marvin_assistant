from backend.services.chat_api.conversations import Conversation


class PromptProgramadorPython:
    @staticmethod
    def get():
        return """
        Olá seu nome é Bella.
        Atue como especialista em programação Python, arquitetura de software, POO, Design Patterns e Clean Code.
        Responda cordialmente a todas as perguntas relacionadas a estes tópicos.
        Caso ela não seja destes assuntos diga que não tem conhecimento sobre isso.  
        Sempre crie respostas resumidas para que sejam lidas rapidamente.
        """


class PromptEspecialistaSantoTomas:
    @staticmethod
    def get():
        return """
        Olá seu nome é Bella.
        Atue como especialista na história, teologia e filosofia de Santo Tomás de Aquino.
        Responda cordialmente a todas as perguntas relacionadas a estes tópicos.
        Caso ela não seja destes assuntos diga que não tem conhecimento sobre isso.  
        Sempre crie respostas resumidas para que sejam lidas rapidamente.
        """


class ConversationService:
    def __init__(self, conversation: Conversation, llm_api_service):
        self._llm_api_service = llm_api_service
        self._conversation = conversation

    def get_conversation(self):
        return self._conversation.get_messages_json(as_str=False)

    def post_conversation_message(self, message):
        if not self._conversation.get_messages():
            self._conversation.post_system_message(PromptEspecialistaSantoTomas.get())

        # Adiciona a mensagem humana recebida.
        self._conversation.post_human_message(message)

        # Manda a nova mensagem do usuário para o LLM Service.
        conversation = self._conversation.get_messages_json(as_str=False)
        content = self._llm_api_service.post(conversation)
        # Converte a resposta que chega em tipo byte.
        result = self.adjust_content(content)
        self._conversation.post_ai_message(result)

        # Devolve a conversa atualizada com a resposta da IA.
        return self._conversation.get_messages_json(as_str=False)

    @staticmethod
    def adjust_content(content):
        result = content.decode("utf-8").strip('"')
        result = result.replace('\\n', ' ')
        result = result.replace('\\', '')
        return result
