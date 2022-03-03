import pygame
from pygame import Surface
from lib.constants import *
from models.World import World


class Player:
    def __init__(self, screen: Surface, world: World, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.screen = screen
        self.world = world
        for i in range(1, 5):
            img_right = pygame.transform.scale(pygame.image.load(f'assets/img/guy{i}.png'), (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        images = self.images_right if self.direction == 1 else self.images_left

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped is False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] is False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] is False and key[pygame.K_RIGHT] is False:
            self.counter = 0
            self.index = 0
            self.image = images[self.index]

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(images):
                self.index = 0
            self.image = images[self.index]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in self.world.tile_list:
            # x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground - jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground - falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
