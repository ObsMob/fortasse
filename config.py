from enum import Enum


BOARD_DEPTH = 3
FULLWIDTH_DIGITS = ["０","１","２","３","４","５","６","７","８","９"]

class Tile_Shape(Enum):
    #TRI = 3
    SQ = 4
    #HEX = 6

class Text_Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    GREY = "\033[90m"
    RESET = "\033[0m"

class Symbol_Icon(Enum):
    EXPLODE = "💥"
    BOMB = "💣"
    CORRECT = "✅"
    INCORRECT = "❌"
    FLAG = "🚩"
    UNKNOWN= "⬜"
    DIGITS = FULLWIDTH_DIGITS

class Resolution(Enum):
    RES_480 = (854, 480)
    RES_720 = (1280, 720)
    RES_900 = (1600, 900)
    RES_1080 = (1920, 1080)
    RES_2K = (2560, 1440)
    RES_4K = (3840, 2160)

