import pygame
from pygame import Surface
from lib.constants import *


class Player:
    def __init__(self, screen: Surface, x, y):
        self.screen = screen
        img = pygame.image.load('assets/img/guy1.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped is False:
            self.vel_y = -15
            self.jumped = True
        elif key[pygame.K_SPACE]:
            self.jumped = False
        elif key[pygame.K_LEFT]:
            dx -= 5
        elif key[pygame.K_RIGHT]:
            dx += 5

        self.vel_y += 1
        if self.vel_y > 20:
            self.vel_y = 20
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        self.screen.blit(self.image, self.rect)

