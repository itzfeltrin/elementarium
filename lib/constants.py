from enum import IntEnum

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

TILE_SIZE = 50


class TileElement(IntEnum):
    DIRT = 1
    GRASS = 2
    ENEMY = 3
    LAVA = 6
    EXIT = 8
