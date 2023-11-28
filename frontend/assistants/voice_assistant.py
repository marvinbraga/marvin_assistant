import asyncio
import os.path
import threading
import warnings

import aiohttp
import pygame

from frontend.assistants.events import SEND_COMMAND_MESSAGE_EVENT, send_command_event, READ_CONTENT_MESSAGE_EVENT
from frontend.audio.audio_to_text import AudioTranscript
from frontend.audio.players import AudioPlayer
from frontend.chats.basic_ui import ChatUI
from frontend.services.chat_api import ChatApi
from frontend.tts.eleven_labs.producers import VoiceProducer
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
warnings.filterwarnings('ignore')


def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# Em algum lugar no seu código de inicialização
async_loop = asyncio.new_event_loop()
threading.Thread(target=start_async_loop, args=(async_loop,), daemon=True).start()


class VoiceAssistant:
    BASE_COLOR = (64, 64, 64)
    RECORDING_COLOR = (144, 238, 144)

    def __init__(self, audio_recorder, audio_loader, tts_api):
        pygame.init()
        pygame.display.set_caption("Assistente de Voz")
        self.user = "marcus"
        self.conversation = "02"
        self.screen = pygame.display.set_mode((640, 480))
        self.chat_ui = ChatUI(self.screen)
        self.tts_api = tts_api
        self.audio_recorder = audio_recorder
        self.audio_loader = audio_loader
        self.running = True
        self.is_recording = False

    def run(self):
        while self.running:
            current_color = self.RECORDING_COLOR if self.is_recording else self.BASE_COLOR
            self.screen.fill(current_color)
            self.chat_ui.draw()
            self.handle_events()
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.start_recording()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.stop_recording()
            elif event.type == SEND_COMMAND_MESSAGE_EVENT:
                self.send_command()
            elif event.type == READ_CONTENT_MESSAGE_EVENT:
                content = event.content
                self.read_content(content)

    def start_recording(self):
        self.is_recording = self.audio_recorder.start().is_recording
        return self

    def stop_recording(self):
        self.is_recording = self.audio_recorder.stop().is_recording
        # Cria evento para envio de comando para o back-end.
        pygame.event.post(send_command_event)
        return self

    def send_command(self):
        command = self._transcribe_audio()
        self._display_transcribed_message(command)
        self._remove_audio_file()

        # Inicia a tarefa assíncrona
        future = asyncio.run_coroutine_threadsafe(
            self.async_send_message_to_chat(
                os.environ["CHAT_HOST"],
                os.environ["CHAT_PORT"],
                self.user,
                self.conversation,
                command
            ), async_loop)

        # Aguarda a conclusão da tarefa assíncrona e obtém a resposta
        try:
            response = future.result(timeout=10)
        except asyncio.TimeoutError:
            print("A operação demorou muito e foi cancelada.")
            return self
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return self

        assistant_response = self._extract_response_message(response)
        self._display_assistant_message(assistant_response)

        self.send_read(content=assistant_response)
        return self

    def _transcribe_audio(self):
        docs = AudioTranscript(loader=self.audio_loader).execute().docs
        return "".join([doc.page_content for doc in docs])

    def _display_transcribed_message(self, message):
        self.chat_ui.add_message(f"User: {message}")

    def _remove_audio_file(self):
        try:
            os.remove(self.audio_recorder.recorder.COMMAND_OUTPUT_FILENAME)
        except OSError as e:
            print(f"Error: {e.strerror}")

    def _send_message_to_chat(self, message):
        chat_api = ChatApi(host=os.environ["CHAT_HOST"], port=os.environ["CHAT_PORT"])
        return chat_api.post(user_id=self.user, conversation_id=self.conversation, message=message)

    @staticmethod
    async def async_send_message_to_chat(host, port, user_id, conversation_id, message):
        async with aiohttp.ClientSession() as session:
            # Substitua 'url' pela URL correta da sua API
            url = f"http://{host}:{port}/api_endpoint"
            data = {'user_id': user_id, 'conversation_id': conversation_id, 'message': message}
            async with session.post(url, json=data) as response:
                return await response.json()

    @staticmethod
    def _extract_response_message(response):
        conversation = response.get("conversation", {})
        messages = conversation.get("messages", [])
        msg = messages[-1].get("content") if messages else "No response received"
        return msg

    def _display_assistant_message(self, message):
        self.chat_ui.add_message(f"Assistant: {message}")

    def send_read(self, content):
        # Executando a leitura da resposta da API.
        data = {"content": content}
        read_content_event = pygame.event.Event(
            READ_CONTENT_MESSAGE_EVENT,
            data,
            message="Evento para executar a leitura do conteúdo da resposta do back-end.",
        )
        pygame.event.post(read_content_event)
        return self

    def read_content(self, content):
        # Recupera o áudio via API.
        response = self.tts_api.get_audio(message=content)
        # Executa o arquivo de áudio.
        filename = os.path.normpath(VoiceProducer(response.content).make().out_content_file)
        AudioPlayer(filename).execute()
        return self
