import pygame
from lib.constants import TILE_SIZE


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/exit.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

