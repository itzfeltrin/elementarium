import pygame
from engine import screen
from lib.constants import SCREEN_WIDTH, SCREEN_HEIGHT

font_path = 'assets/font/rainyhearts.ttf'
font_60 = pygame.font.Font(font_path, 60)
font_120 = pygame.font.Font(font_path, 120)


def draw_text(text, font_to_use, color, x, y):
    img = font_to_use.render(text, True, color)
    screen.blit(img, (x, y))


def center_pos(img: pygame.Surface):
    center_x = SCREEN_WIDTH // 2 - img.get_width() // 2
    center_y = SCREEN_HEIGHT // 2 - img.get_height() // 2
    return center_x, center_y


# load sounds
jump_fx = pygame.mixer.Sound('assets/sound/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('assets/sound/game_over.wav')
game_over_fx.set_volume(0.5)
