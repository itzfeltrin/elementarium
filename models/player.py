import os

import pygame
from engine import screen
from lib.shared import draw_text, font, jump_fx, game_over_fx
from lib.constants import BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from entities.groups import blob_group, lava_group, exit_group, platform_group, element_group, power_group
from models.power_ball import Power

game_over_img = pygame.image.load('assets/img/elements/game-over.png').convert_alpha()


class Player:
    # Feel like this is poorly structured
    def __init__(self, x, y, element='normal'):
        # initialize all properties as none so pylint doesn't complain about them being defined outside the __init__
        # method
        self.images = None
        self.index = None
        self.counter = None
        self.dead_image = None
        self.image = None
        self.rect = None
        self.width = None
        self.height = None
        self.vel_y = None
        self.jumped = None
        self.direction = None
        self.in_air = None
        self.element = None
        self.shooting = None
        self.reset(x, y, element)

    def update(self, tile_list: int, game_over: int):
        dx = 0
        dy = 0
        walk_cooldown = 5
        collision_threshold = 20

        if game_over == 0:
            images = self.images[self.element][1] if self.direction == 1 else self.images[self.element][0]

            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped is False and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_UP] is False:
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

            if key[pygame.K_SPACE] and self.element != 'normal' and self.shooting is False:
                power_group.add(Power(self.element, self.rect.left if self.direction == -1 else self.rect.right, self.rect.centery, self.direction))
                self.shooting = True
            if key[pygame.K_SPACE] is False and self.shooting:
                self.shooting = False

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
            for tile in tile_list:
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
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with exit gates
            if pygame.sprite.spritecollide(self, exit_group, False) and self.element != 'normal':
                game_over = 1

            # check for collision with platforms
            for platform in platform_group:
                # x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below platform
                    if abs(self.rect.top + dy - platform.rect.bottom) < collision_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs(self.rect.bottom + dy - platform.rect.top) < collision_threshold:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideways with platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # check for collision with elements
            for element in element_group:
                if element.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    if pygame.key.get_pressed()[pygame.K_e]:
                        self.element = element.name
            # update player pos
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            screen.blit(game_over_img, (SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))
            # draw_text('GAME OVER!', font, BLUE, (SCREEN_WIDTH // 2) - 200, SCREEN_HEIGHT // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y, element):
        self.index = 0
        self.counter = 0
        asset_folder = 'assets/img/player'
        # existem 4 estados de imagem para cada personagem
        elements = ['normal', 'fire', 'water', 'nature']
        player_images = {}
        for element_name in elements:
            temp_images = ([], [])
            for i in range(0, 3):
                img = pygame.image.load(os.path.join(asset_folder, f'{element_name}-{i}.png')).convert_alpha()
                sprite_img = img.subsurface(230, 200, 420, 570)
                img_right = pygame.transform.scale(sprite_img, (50, 68))
                img_left = pygame.transform.flip(img_right, True, False)
                temp_images[0].append(img_left)
                temp_images[1].append(img_right)
            player_images[element_name] = temp_images
        self.images = player_images
        self.dead_image = pygame.image.load('assets/img/elements/ghost.png')
        self.element = element
        self.image = self.images[self.element][1][self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.image.get_width() * 0.8
        self.width = self.rect.width
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        self.direction = 1
        self.shooting = False
