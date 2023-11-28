import asyncio
import logging
import os.path
import threading
import warnings

import pygame
from dotenv import load_dotenv, find_dotenv

from frontend.assistants.events import SEND_COMMAND_MESSAGE_EVENT, send_command_event, READ_CONTENT_MESSAGE_EVENT
from frontend.audio.audio_to_text import AudioTranscript
from frontend.audio.players import AudioPlayer
from frontend.chats.basic_ui import ChatUI
from frontend.services.chat_api import ChatApi
from frontend.tts.eleven_labs.producers import VoiceProducer

load_dotenv(find_dotenv())
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logging.info("Teste de log voice_assistant.")


def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


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
                asyncio.run_coroutine_threadsafe(self.send_command(), async_loop)
            elif event.type == READ_CONTENT_MESSAGE_EVENT:
                content = event.content
                asyncio.run_coroutine_threadsafe(self.read_content(content), async_loop)

    def start_recording(self):
        self.is_recording = self.audio_recorder.start().is_recording
        return self

    def stop_recording(self):
        self.is_recording = self.audio_recorder.stop().is_recording
        # Cria evento para envio de comando para o back-end.
        pygame.event.post(send_command_event)
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

    async def send_command(self):
        logging.info("INICIANDO: Transcrição do comando.")
        command = self._transcribe_audio()
        self._display_transcribed_message(command)
        self._remove_audio_file()
        logging.info("FINALIZANDO: Transcrição do comando.")

        # Faz a chamada assíncrona e aguarda a resposta
        logging.info("INICIANDO: response = await self._send_message_to_chat(command)")
        response = await self._send_message_to_chat(command)
        logging.info("FINALIZANDO: response = await self._send_message_to_chat(command)")

        assistant_response = self._extract_response_message(response)
        self._display_assistant_message(assistant_response)

        self.send_read(content=assistant_response)

    async def _send_message_to_chat(self, message):
        chat_api = ChatApi(host=os.environ["CHAT_HOST"], port=os.environ["CHAT_PORT"])
        return await chat_api.post(user_id=self.user, conversation_id=self.conversation, message=message)

    async def read_content(self, content):
        logging.info("INICIANDO: o TTS.")
        # Recupera o áudio via API.
        audio_data = await self.tts_api.get_audio(message=content)
        logging.info("FINALIZANDO: o TTS.")
        # Executa o arquivo de áudio.
        logging.info("INICIANDO: Execução do áudio.")
        filename = os.path.normpath(VoiceProducer(audio_data).make().out_content_file)
        AudioPlayer(filename).execute()
        logging.info("FINALIZANDO: Execução do áudio.")
