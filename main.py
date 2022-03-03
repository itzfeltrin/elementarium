import pygame
from lib.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, WORLD_DATA
from models.button import Button
from models.world import World
from models.player import Player

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

# load images
sun_img = pygame.image.load('assets/img/sun.png')
bg_img = pygame.image.load('assets/img/sky.png')
restart_img = pygame.image.load('assets/img/restart_btn.png')
start_img = pygame.image.load('assets/img/start_btn.png')
exit_img = pygame.image.load('assets/img/exit_btn.png')

fps = 60
main_menu = True
game_over = 0
running = True

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
world = World(screen, blob_group, lava_group, WORLD_DATA)
player = Player(100, SCREEN_HEIGHT - (TILE_SIZE + 80), screen, world, blob_group, lava_group)

# create buttons
restart_button = Button(
    SCREEN_WIDTH // 2 - restart_img.get_width() // 2,
    SCREEN_HEIGHT // 2 - restart_img.get_height() // 2,
    restart_img
)
start_button = Button(
    SCREEN_WIDTH // 2 - start_img.get_width() // 2 - start_img.get_width() // 1.5,
    SCREEN_HEIGHT // 2 - start_img.get_height() // 2,
    start_img
)
exit_button = Button(
    SCREEN_WIDTH // 2 - exit_img.get_width() // 2 + exit_img.get_width() // 1.5,
    SCREEN_HEIGHT // 2 - exit_img.get_height() // 2,
    exit_img
)

clock = pygame.time.Clock()

while running:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu is True:
        if exit_button.draw(screen):
            running = False
        if start_button.draw(screen):
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
        blob_group.draw(screen)

        lava_group.update()
        lava_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw(screen):
                player.reset(100, SCREEN_HEIGHT - (TILE_SIZE + 80), screen, world, blob_group, lava_group)
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
