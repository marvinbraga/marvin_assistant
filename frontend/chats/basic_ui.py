import pygame
import textwrap

WHITE = (255, 255, 255)
BASE_COLOR = (57, 115, 35)
RECORDING_COLOR = (144, 238, 144)


class ChatUI:

    def __init__(self, screen, user_name, text_color=(0, 0, 0)):
        self.user_name = user_name
        self.screen = screen
        self._font_size = 16
        self.font = pygame.font.SysFont(name="Hack Nerd Font Mono", size=self._font_size)
        self.text_color = text_color
        self.button_color = BASE_COLOR
        self.button_rect = None
        self._chat_log = []
        self._is_pressed = False

    def render_text(self, text, pos, width):
        words = textwrap.wrap(text, width)
        y_offset = 0
        for word in words:
            word_surface = self.font.render(word, True, self.text_color)
            self.screen.blit(word_surface, (pos[0], pos[1] + y_offset))
            y_offset += word_surface.get_height()

    def draw_button(self, text, pos, size):
        self.button_rect = pygame.Rect(*pos, *size)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        text_surface = self.font.render(text, True, self.text_color)
        self.screen.blit(text_surface, (pos[0] + 10, pos[1] + 10))

    def is_button_pressed(self, event):
        if self.button_rect is None:
            result, self._is_pressed = False, False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                result, self._is_pressed = self.button_rect.collidepoint(event.pos), True
            else:
                result, self._is_pressed = self.button_rect.collidepoint(event.pos), False
        return result

    def print_user_message(self, message):
        msg = f"{self.user_name}: {message}"
        self.render_text(msg, (50, 50), 70)
        return self

    def print_ai_message(self, message):
        msg = f"Resposta da IA: {message}"
        self.render_text(msg, (50, 150), 70)
        return self

    def update(self):
        self.screen.fill(WHITE)
        if self._chat_log and len(self._chat_log) % 2 == 1:
            message = self._chat_log[-1]
            self.print_user_message(message)
        elif self._chat_log and len(self._chat_log) % 2 == 0:
            self.print_user_message(self._chat_log[-2]).print_ai_message(self._chat_log[-1])

        btn_text = "Pressione para enviar mensagem"
        self.button_color = RECORDING_COLOR if self._is_pressed else BASE_COLOR
        button_width, button_height = 318, 40
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = 550
        self.draw_button(btn_text, (button_x, button_y), (button_width, button_height))
        return self

    def add_message(self, message):
        self._chat_log.append(message)
        return self
