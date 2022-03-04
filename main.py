import pygame
import pickle
from os import path
from engine import screen
from lib.constants import SCREEN_HEIGHT, TILE_SIZE
from ui import start_button, exit_button, restart_button
from entities.world import world
from entities.groups import blob_group, lava_group, exit_group
from models.world import World
from models.player import Player

clock = pygame.time.Clock()
fps = 60

# load images
sun_img = pygame.image.load('assets/img/sun.png')
bg_img = pygame.image.load('assets/img/sky.png')

main_menu = True
game_over = 0
running = True
level = 1
max_levels = 7

player = Player(100, SCREEN_HEIGHT - (TILE_SIZE + 80))


# function to reset level
def reset_level(new_level):
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()

    if path.exists(f'assets/level{new_level}_data') is False:
        return world

    pickle_in = open(f'assets/level{new_level}_data', 'rb')
    new_world_data = pickle.load(pickle_in)
    player.reset(100, SCREEN_HEIGHT - (TILE_SIZE + 80))
    return World(new_world_data)


while running:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu is True:
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
        blob_group.draw(screen)

        lava_group.update()
        lava_group.draw(screen)

        exit_group.update()
        exit_group.draw(screen)

        game_over = player.update(world.tile_list, game_over)

        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
        elif game_over == 1:
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_button.draw():
                    level = 0
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
