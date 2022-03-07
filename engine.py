import pygame
from pygame import mixer
from lib.constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

pygame.mixer.music.load('assets/sound/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
