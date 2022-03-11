import pygame
import pickle
from os import path
from engine import screen
from lib.constants import SCREEN_HEIGHT, TILE_SIZE, SCREEN_WIDTH
from lib.shared import font_120, center_pos, font_60
from ui import start_button, exit_button, restart_button
from entities.world import world
from entities.groups import blob_group, lava_group, exit_group, platform_group, element_group, power_group, \
    explosion_group
from models.world import World
from models.player import Player
from models.element import Element

clock = pygame.time.Clock()
fps = 60

# load images
bg_img = pygame.transform.scale(pygame.image.load('assets/img/bg/0.jpg').convert(), (SCREEN_WIDTH * 2, SCREEN_HEIGHT))
ifrs_img = pygame.image.load('assets/img/elements/ifrs.png').convert_alpha()
cc_img = pygame.image.load('assets/img/elements/computacao.png').convert_alpha()

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
        screen.blit(cc_img, (SCREEN_WIDTH - TILE_SIZE * 2, TILE_SIZE))
        screen.blit(ifrs_img, (SCREEN_WIDTH - TILE_SIZE * 4, TILE_SIZE))

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
        power_group.update(world.tile_list)
        power_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)

        game_over = player.update(world.tile_list, game_over)

        if level == 1:
            tutorial_text_img_1 = font_60.render(
                "Use as setas para se mover", True,
                (31, 23, 0))
            tutorial_text_img_2 = font_60.render(
                "E para selecionar um elemento", True,
                (31, 23, 0))
            tutorial_text_img_3 = font_60.render(
                "Espaço para atirar", True,
                (31, 23, 0))
            screen.blit(tutorial_text_img_1, (TILE_SIZE * 2, TILE_SIZE * 2))
            screen.blit(tutorial_text_img_2, (TILE_SIZE * 2, TILE_SIZE * 3))
            screen.blit(tutorial_text_img_3, (TILE_SIZE * 2, TILE_SIZE * 4))

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
                you_win_img = font_120.render("YOU WIN !!", True, (255, 186, 3))
                you_win_img_pos = (center_pos(you_win_img))
                you_win_img_shadow = font_120.render("YOU WIN !!", True, (31, 23, 0))
                screen.blit(you_win_img_shadow, (you_win_img_pos[0] + 4, you_win_img_pos[1] + 4))
                screen.blit(you_win_img, you_win_img_pos)
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
