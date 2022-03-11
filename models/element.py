import pygame

from lib.constants import SCREEN_HEIGHT, TILE_SIZE, SCREEN_WIDTH


class Element(pygame.sprite.Sprite):
    def __init__(self, name, index):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        image = pygame.image.load(f'assets/img/elements/{name}.png').convert_alpha()
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2 - self.image.get_width() // 2 - 80 * index, SCREEN_HEIGHT - (TILE_SIZE + 96))
