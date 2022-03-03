import pygame
from pygame import Surface
from pygame.sprite import Group
from lib.constants import TILE_SIZE, TileElement
from models.enemy import Enemy
from models.lava import Lava


class World:
    def __init__(self, screen: Surface, blob_group: Group, lava_group:Group, data):
        self.screen = screen
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('assets/img/dirt.png')
        grass_img = pygame.image.load('assets/img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == TileElement.DIRT:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == TileElement.GRASS:
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == TileElement.ENEMY:
                    blob = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE + 15)
                    blob_group.add(blob)
                elif tile == TileElement.LAVA:
                    lava = Lava(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            pygame.draw.rect(self.screen, (255, 255, 255), tile[1], 2)