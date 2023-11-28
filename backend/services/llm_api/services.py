from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage


class LLMConnection:

    def __init__(self, data):
        self._data = data
        self._messages: list[BaseMessage] = []
        self._memory = ConversationBufferMemory(return_messages=True, ai_prefix="AI Assistant")
        self._prompt = None
        self._message = None
        self._output = ""

    @property
    def output(self):
        return self._output

    def _create_messages(self, conversation):
        role_class_map = {
            "ai": AIMessage,
            "human": HumanMessage,
            "system": SystemMessage
        }
        self._messages = [role_class_map[message["role"]](content=message["content"]) for message in conversation]
        return self

    def _create_prompt(self):
        system_message = self._messages.pop(0)
        prompt = system_message.content + """
        
        Conversa atual:
        {history}
        
        AI Assistant: 
        {input}
        """
        self._prompt = PromptTemplate(input_variables=["history", "input"], template=prompt)
        return self

    def _update_memory(self):
        # Limpa a memória.
        self._memory.load_memory_variables({})
        # Atualiza a memória
        data = []
        for msg in self._messages:
            if isinstance(msg, HumanMessage):
                if len(data):
                    data = []
                data.append({"input": msg.content})
                continue
            if isinstance(msg, AIMessage):
                data.append({"output": msg.content})

            self._memory.save_context(*data)
            data = []

        return self

    def get_message(self):
        # Recupera a última mensagem recebida
        self._message = self._messages[-1]
        return self

    def send(self):
        self._create_messages(
            self._data["conversation"]["messages"]
        )._create_prompt()._update_memory().get_message()
        llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo")
        chain = ConversationChain(
            llm=llm,
            memory=self._memory,
            prompt=self._prompt,
            # max_tokens=300,
        )
        self._output = chain.predict(input=self._message.content)
        return self
