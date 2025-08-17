from enum import Enum


BOARD_DEPTH = 3

class Tile_Shape(Enum):
    TRI = 3
    SQ = 4
    HEX = 6

class Resolution(Enum):
    RES_480 = (854, 480)
    RES_720 = (1280, 720)
    RES_900 = (1600, 900)
    RES_1080 = (1920, 1080)
    RES_2K = (2560, 1440)
    RES_4K = (3840, 2160)
