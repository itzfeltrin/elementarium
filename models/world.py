import os

import pygame
from engine import screen
from entities.groups import blob_group, lava_group, exit_group, platform_group
from lib.constants import TILE_SIZE, TileElement
from models.enemy import Enemy
from models.lava import Lava
from models.exit import Exit
from models.platform import Platform


class World:
    def __init__(self, data):
        self.tile_list = []

        # load images
        tiles_folder = 'assets/img/tiles'

        dirt_center_img = pygame.image.load(os.path.join(tiles_folder, '5.png'))
        grass_left_corner_img = pygame.image.load(os.path.join(tiles_folder, '1.png'))
        grass_right_corner_img = pygame.image.load(os.path.join(tiles_folder, '3.png'))
        grass_center_img = pygame.image.load('assets/img/tiles/2.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == TileElement.DIRT:
                    img = pygame.transform.scale(dirt_center_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == TileElement.GRASS:
                    if data[row_count][col_count - 1] == 0 and data[row_count][col_count + 1] != 0:
                        img = pygame.transform.scale(grass_left_corner_img, (TILE_SIZE, TILE_SIZE))
                    elif data[row_count][col_count + 1] == 0 and data[row_count][col_count - 1] != 0:
                        img = pygame.transform.scale(grass_right_corner_img, (TILE_SIZE, TILE_SIZE))
                    else:
                        img = pygame.transform.scale(grass_center_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == TileElement.ENEMY:
                    blob = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE - 15)
                    blob_group.add(blob)
                elif tile == TileElement.HORIZONTAL_PLATFORM:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0)
                    platform_group.add(platform)
                elif tile == TileElement.VERTICAL_PLATFORM:
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1)
                    platform_group.add(platform)
                elif tile == TileElement.LAVA:
                    lava = Lava(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
                    lava_group.add(lava)
                elif tile == TileElement.EXIT:
                    exit_gate = Exit(col_count * TILE_SIZE, row_count * TILE_SIZE - (TILE_SIZE // 2))
                    exit_group.add(exit_gate)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
