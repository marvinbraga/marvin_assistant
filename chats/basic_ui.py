import pygame

pygame.init()


class ChatUI:
    def __init__(self, screen):
        self.screen = screen
        self.chat_log = []
        self.font = pygame.font.Font(None, 36)

    def add_message(self, message):
        self.chat_log.append(message)

    def draw(self):
        y = 20
        for message in self.chat_log:
            text_surface = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, y))
            y += 40
