import pygame
from pygame import Surface
from pygame.sprite import Group
from lib.constants import *
from models.world import World


class Player:
    def __init__(self, x, y, screen: Surface, world: World, blob_group: Group, lava_group: Group):
        # initialize all properties as none so pylint doesn't complain about them being defined outside the __init__
        # method
        self.images_right = None
        self.images_left = None
        self.index = None
        self.counter = None
        self.screen = None
        self.world = None
        self.blob_group = None
        self.lava_group = None
        self.dead_image = None
        self.image = None
        self.rect = None
        self.width = None
        self.height = None
        self.vel_y = None
        self.jumped = None
        self.direction = None
        self.in_air = None
        self.reset(x, y, screen, world, blob_group, lava_group)

    def update(self, game_over: int):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            images = self.images_right if self.direction == 1 else self.images_left

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped is False and not self.in_air:
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
            self.in_air = True
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
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, self.blob_group, False):
                game_over = -1

            # check for collision with lava
            if pygame.sprite.spritecollide(self, self.lava_group, False):
                game_over = -1

            # update player pos
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)

        return game_over
    
    def reset(self, x, y, screen: Surface, world: World, blob_group: Group, lava_group: Group):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.screen = screen
        self.world = world
        self.blob_group = blob_group
        self.lava_group = lava_group
        for i in range(1, 5):
            img_right = pygame.transform.scale(pygame.image.load(f'assets/img/guy{i}.png'), (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('assets/img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        self.direction = 1
