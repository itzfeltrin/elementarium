import pygame
from engine import screen

font = pygame.font.SysFont('ubuntu', 70)
font_score = pygame.font.SysFont('ubuntu', 30)


def draw_text(text, font_to_use, color, x, y):
    img = font_to_use.render(text, True, color)
    screen.blit(img, (x, y))


# load sounds
coin_fx = pygame.mixer.Sound('assets/img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('assets/img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('assets/img/game_over.wav')
game_over_fx.set_volume(0.5)
