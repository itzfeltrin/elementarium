import pygame
from pygame.locals import *

from lib.constants import *
from models.Player import Player

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()

    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    all_sprites.draw(screen)

    pygame.display.flip()

print("Jogo finalizado")
pygame.quit()
