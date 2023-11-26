import pygame


class AudioPlayer:

    def __init__(self, file_path):
        self._file_path = file_path

    def execute(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self._file_path)
        pygame.mixer.music.play()
        return self
