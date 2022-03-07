import os

import pygame
from models.button import Button
from lib.constants import SCREEN_WIDTH, SCREEN_HEIGHT

buttons_folder = 'assets/img/buttons'

restart_img = pygame.image.load(os.path.join(buttons_folder, 'restart_btn.png'))
start_img = pygame.image.load(os.path.join(buttons_folder, 'start_btn.png'))
exit_img = pygame.image.load(os.path.join(buttons_folder, 'exit_btn.png'))

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
