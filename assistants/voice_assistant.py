import os.path

import pygame

from audio.audio_to_text import AudioTranscript
from chats.basic_ui import ChatUI

SEND_COMMAND_MESSAGE_EVENT = pygame.USEREVENT + 100
send_command_event = pygame.event.Event(
    SEND_COMMAND_MESSAGE_EVENT,
    message="Evento para processar e enviar o comando ao back-end.",
)


class VoiceAssistant:
    BASE_COLOR = (64, 64, 64)
    RECORDING_COLOR = (144, 238, 144)

    def __init__(self, audio_recorder, audio_loader):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Assistente de Voz")
        self.chat_ui = ChatUI(self.screen)
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
        self.chat_ui.add_message(f'User: {command}')
        # Remove o arquivo temporário do comando de voz.
        os.remove(self.audio_recorder.recorder.COMMAND_OUTPUT_FILENAME)
        return self
