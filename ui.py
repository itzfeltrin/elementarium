import pygame
from models.button import Button
from lib.constants import SCREEN_WIDTH, SCREEN_HEIGHT

restart_img = pygame.image.load('assets/img/restart_btn.png')
start_img = pygame.image.load('assets/img/start_btn.png')
exit_img = pygame.image.load('assets/img/exit_btn.png')

# create buttons
restart_button = Button(
    SCREEN_WIDTH // 2 - restart_img.get_width() // 2,
    SCREEN_HEIGHT // 2 - restart_img.get_height() // 2,
    restart_img
)
start_button = Button(
    SCREEN_WIDTH // 2 - start_img.get_width() // 2 - start_img.get_width() // 1.5,
    SCREEN_HEIGHT // 2 - start_img.get_height() // 2,
    start_img
)
exit_button = Button(
    SCREEN_WIDTH // 2 - exit_img.get_width() // 2 + exit_img.get_width() // 1.5,
    SCREEN_HEIGHT // 2 - exit_img.get_height() // 2,
    exit_img
)
