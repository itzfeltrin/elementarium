import random

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        enemy_type = random.randint(1, 3)
        for i in range(2):
            image = pygame.image.load(f'assets/img/elements/enemy-type-{enemy_type}-{i + 1}.png').convert_alpha()
            img_right = pygame.transform.scale(image, (96, 68))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.index = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width * 0.66
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_cooldown = 0

    def update(self):
        if self.move_cooldown == 0:
            self.move_cooldown = 2
            images_to_use = self.images_right if self.move_direction == 1 else self.images_left
            self.index += 1
            if self.index == len(images_to_use):
                self.index = 0
            self.image = images_to_use[self.index]
        else:
            self.move_cooldown -= 0.25
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
