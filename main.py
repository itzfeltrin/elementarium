import pygame
import pickle
from os import path
from engine import screen
from lib.shared import draw_text, font_score, font, coin_fx
from lib.constants import SCREEN_HEIGHT, TILE_SIZE, BLACK, BLUE, SCREEN_WIDTH
from ui import start_button, exit_button, restart_button
from entities.world import world
from entities.groups import blob_group, lava_group, exit_group, coin_group, platform_group
from models.world import World
from models.player import Player

clock = pygame.time.Clock()
fps = 60

# load images
sun_img = pygame.image.load('assets/img/sun.png')
bg_img = pygame.image.load('assets/img/sky.png')
coin_img = pygame.transform.scale(pygame.image.load('assets/img/coin.png'), (TILE_SIZE // 2, TILE_SIZE // 2))

# game variables
main_menu = True
running = True
game_over = 0
level = 3
max_levels = 7
score = 0

player = Player(100, SCREEN_HEIGHT - (TILE_SIZE + 80))


# function to reset level
def reset_level(new_level):
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()

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
            platform_group.update()
            # update score
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text(f'X {score}', font_score, BLACK, TILE_SIZE - 10, TILE_SIZE - TILE_SIZE // 2 - 30 / 2)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)

        screen.blit(coin_img, (TILE_SIZE // 2 - coin_img.get_width() // 2, TILE_SIZE // 2 - coin_img.get_height() // 2))

        game_over = player.update(world.tile_list, game_over)

        # if player has died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        elif game_over == 1:
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
