import pygame

# load power images
from entities.groups import blob_group, platform_group
from lib.constants import SCREEN_WIDTH, TILE_SIZE

elements = ['fire', 'water', 'nature']

images = {}
sounds = {}
for element_name in elements:
    image = pygame.image.load(f'assets/img/elements/power-{element_name}.png').convert_alpha()
    images[element_name] = pygame.transform.scale(image, (24, 24))
    explosion_fx = pygame.mixer.Sound(f'assets/sound/{element_name}-explosion.wav')
    explosion_fx.set_volume(0.5)
    sounds[element_name] = explosion_fx

class Power(pygame.sprite.Sprite):
    def __init__(self, element, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.element = element
        self.image = images[element]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def explode(self):
        sounds[self.element].play()
        self.kill()

    def update(self, tile_list):
        vel_x = 7.5
        dx = vel_x * self.direction
        right_edge = SCREEN_WIDTH - TILE_SIZE
        left_edge = TILE_SIZE
        if self.rect.right + dx >= right_edge:
            self.rect.x += right_edge - self.rect.x + dx
            self.explode()
        elif self.rect.left + dx <= left_edge:
            self.rect.x += self.rect.x + dx - left_edge
            self.explode()
        else:
            self.rect.x += dx

        if self.alive():
            if pygame.sprite.spritecollide(self, blob_group, True):
                self.explode()
            elif pygame.sprite.spritecollide(self, platform_group, False):
                self.explode()
            else:
                for tile in tile_list:
                    if tile[1].colliderect(self.rect):
                        self.explode()
