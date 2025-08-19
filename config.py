from enum import Enum


FIRST_LOAD = True

BOARD_DEPTH = 3
TILE_SHAPE = Tile_Shape.SQ
CORNERS = False
RESOLUTION = Resolutions.RES_1080

FULLWIDTH_DIGITS = ["０","１","２","３","４","５","６","７","８","９"]
TILE_WIDTH = 2

class Tile_Shape(Enum):
    TRI = "Triangle"
    SQ = "Square"
    HEX = "Hexagon"

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
    TOPLEFT = "╔"
    TOPRIGHT = "╗"
    BOTLEFT = "╚"
    BOTRIGHT = "╝"
    TOPTEE = "╦"
    BOTTEE = "╩"
    LEFTTEE = "╠"
    RIGHTTEE = "╣"
    HORIZ = "═"
    VERT = "║"
    TEE = "╬"
    EMPTY = "  "

class Resolutions(Enum):
    # RES_480 = (854, 480)
    # RES_720 = (1280, 720)
    # RES_900 = (1600, 900)
    RES_1080 = "1920x1080"
    RES_2K = "2560x1440"
    RES_4K = "3840x2160"

class Menu(Enum):
    MAIN = "Main Menu"
    EDIT = "Edit Menu"
    DEPTH = "Depth Menu"
    TILE =  "Tile Menu"
    CORNERS = "Corner Menu"
    RES = "Resolution Menu"
