from enum import IntEnum

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

TILE_SIZE = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class TileElement(IntEnum):
    DIRT = 1
    GRASS = 2
    ENEMY = 3
    VERTICAL_PLATFORM = 4
    HORIZONTAL_PLATFORM = 5
    LAVA = 6
    COIN = 7
    EXIT = 8
    