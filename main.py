import random

import pygame
import pickle
from os import path
from engine import screen
from lib.shared import draw_text, font
from lib.constants import SCREEN_HEIGHT, TILE_SIZE, BLUE, SCREEN_WIDTH
from ui import start_button, exit_button, restart_button
from entities.world import world
from entities.groups import blob_group, lava_group, exit_group, platform_group, element_group, power_group
from models.world import World
from models.player import Player
from models.element import Element

clock = pygame.time.Clock()
fps = 60

# load images
bg_img = pygame.transform.scale(pygame.image.load('assets/img/bg/0.jpg').convert(), (SCREEN_WIDTH * 2, SCREEN_HEIGHT))

# game variables
main_menu = True
running = True
game_over = 0
level = 1
max_levels = 7
score = 0

player = Player(100, SCREEN_HEIGHT - (TILE_SIZE + 80), 'normal')


# function to reset level
def reset_level(new_level):
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    if path.exists(f'assets/level{new_level}_data') is False:
        return world

    pickle_in = open(f'assets/level{new_level}_data', 'rb')
    new_world_data = pickle.load(pickle_in)
    player.reset(100, SCREEN_HEIGHT - (TILE_SIZE + 80), player.element)
    return World(new_world_data)


# create elements
element_names = ['fire', 'water', 'nature']
for index, element_name in enumerate(element_names):
    element = Element(element_name, index)
    element_group.add(element)

while running:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    if main_menu is True:
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        element_group.draw(screen)
        power_group.update()
        power_group.draw(screen)

        game_over = player.update(world.tile_list, game_over)

        # if player has died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        elif game_over == 1:
            if level == 1:
                element_group.empty()
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, BLUE, (SCREEN_WIDTH // 2) - 140, SCREEN_HEIGHT // 2)
                if restart_button.draw():
                    level = 0
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
