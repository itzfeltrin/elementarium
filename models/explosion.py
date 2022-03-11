import pygame

images = []

for num in range(1, 6):
    img = pygame.image.load(f"assets/img/elements/exp-{num}.png")
    img = pygame.transform.scale(img, (32, 32))
    images.append(img)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.index = 0
        self.image = images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(images) - 1:
            self.counter = 0
            self.index += 1
            self.image = images[self.index]

        if self.index >= len(images) - 1 and self.counter >= explosion_speed:
            self.kill()
