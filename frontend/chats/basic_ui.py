import pygame

pygame.init()


class ChatUI:
    def __init__(self, screen):
        self.screen = screen
        self.chat_log = []
        self._font_size = 16
        self.font = pygame.font.SysFont(name="Hack Nerd Font Mono", size=self._font_size)

    def add_message(self, message):
        self.chat_log.append(message)

    def draw(self):
        y = 20
        for message in self.chat_log:
            text_surface = self.font.render(message, True, (204, 204, 204))
            self.screen.blit(text_surface, (20, y))
            y += self._font_size + 2
