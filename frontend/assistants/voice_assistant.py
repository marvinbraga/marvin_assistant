import os.path

import pygame

from frontend.assistants.events import SEND_COMMAND_MESSAGE_EVENT, send_command_event, READ_CONTENT_MESSAGE_EVENT
from frontend.audio.audio_to_text import AudioTranscript
from frontend.audio.players import AudioPlayer
from frontend.chats.basic_ui import ChatUI
from frontend.tts.eleven_labs.producers import VoiceProducer


class VoiceAssistant:
    BASE_COLOR = (64, 64, 64)
    RECORDING_COLOR = (144, 238, 144)

    def __init__(self, audio_recorder, audio_loader, tts_api):
        pygame.init()
        pygame.display.set_caption("Assistente de Voz")
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
                # self.read_content(content)

    def start_recording(self):
        self.is_recording = self.audio_recorder.start().is_recording
        return self

    def stop_recording(self):
        self.is_recording = self.audio_recorder.stop().is_recording
        # Cria evento para envio de comando para o back-end.
        pygame.event.post(send_command_event)
        return self

    def send_command(self):
        # Transformando áudio em texto.
        docs = AudioTranscript(loader=self.audio_loader).execute().docs
        command = "".join([d.page_content for d in docs])
        # Apresenta mensagem transcrita.
        self.chat_ui.add_message(f"User: {command}")
        # Remove o arquivo temporário do comando de voz.
        os.remove(self.audio_recorder.recorder.COMMAND_OUTPUT_FILENAME)

        # TODO: Enviar o comando para a API do Chat.
        # TODO: A API do Chat chamará a API do RAG, que retornará uma resposta em texto.
        # TODO: Recupera a resposta em texto e utiliza a função send_read(content=content)
        content = command

        # Imprime a resposta da API do RAG.
        self.chat_ui.add_message(f"Assistant: {content}")
        # Chama a execução da leitura da resposta.
        self.send_read(content=content)
        return self

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
