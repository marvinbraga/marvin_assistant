import json
import os

from dotenv import load_dotenv, find_dotenv
from langchain.memory import RedisChatMessageHistory
from langchain.schema import SystemMessage

load_dotenv(find_dotenv())


class Conversation:

    def __init__(self, session_id):
        redis_url = f"redis://{os.environ['REDIS_HOST']}:6379"
        self._session_id = session_id
        self._memory = RedisChatMessageHistory(
            session_id=session_id,
            url=redis_url,
        )

    def get_messages(self):
        return self._memory.messages

    def post_system_message(self, message: str):
        self._memory.add_message(SystemMessage(content=message))
        return self

    def post_human_message(self, message: str):
        self._memory.add_user_message(message)
        return self

    def post_ai_message(self, message: str):
        self._memory.add_ai_message(message)
        return self

    def get_messages_json(self, to_str=True):
        result = {
            "conversation": {
                "key_id": self._session_id,
                "messages": [
                    {"role": m.type, "content": m.content} for m in self._memory.messages
                ]
            }
        }
        if to_str:
            result = json.dumps(result)
        return result


if __name__ == '__main__':
    c1 = Conversation(session_id="user1-conversation1")
    c2 = Conversation(session_id="user2-conversation1")

    print("TESTES COM USER1 E CONVERSATION1")
    print("--------------------------------")
    print(c1.get_messages())
    c1.post_human_message("Testando envio de mensagem do user1.")
    c1.post_ai_message("Testando envio de resposta da ia para o user c1.")
    print(c1.get_messages())
    print(c1.get_messages_json())

    print("TESTES COM USER2 E CONVERSATION1")
    print("--------------------------------")
    print(c2.get_messages())
