import pygame
from engine import screen

font = pygame.font.SysFont('ubuntu', 70)
font_score = pygame.font.SysFont('ubuntu', 30)


def draw_text(text, font_to_use, color, x, y):
    img = font_to_use.render(text, True, color)
    screen.blit(img, (x, y))