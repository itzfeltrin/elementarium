import pygame

# load power images
from lib.constants import SCREEN_WIDTH, TILE_SIZE

elements = ['fire', 'water', 'nature']
images = {}
for element_name in elements:
    image = pygame.image.load(f'assets/img/elements/power-{element_name}.png').convert_alpha()
    images[element_name] = pygame.transform.scale(image, (24, 24))


class Power(pygame.sprite.Sprite):
    def __init__(self, element, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = images[element]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        vel_x = 7.5
        dx = vel_x * self.direction
        right_edge = SCREEN_WIDTH - TILE_SIZE
        left_edge = TILE_SIZE
        if self.rect.right + dx >= right_edge:
            self.rect.x += right_edge - self.rect.x + dx
            self.kill()
        elif self.rect.left + dx <= left_edge:
            self.rect.x += self.rect.x + dx - left_edge
            self.kill()
        else:
            self.rect.x += dx
