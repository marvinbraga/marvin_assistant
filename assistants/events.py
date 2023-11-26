import pygame

SEND_COMMAND_MESSAGE_EVENT = pygame.USEREVENT + 100
READ_CONTENT_MESSAGE_EVENT = SEND_COMMAND_MESSAGE_EVENT + 1

send_command_event = pygame.event.Event(
    SEND_COMMAND_MESSAGE_EVENT,
    message="Evento para processar e enviar o comando ao back-end.",
)
