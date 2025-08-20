from enum import Enum, auto


FIRST_LOAD = True
FULLWIDTH_DIGITS = ["０","１","２","３","４","５","６","７","８","９"]

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
    TACO = "🌮"
    TROPHY = "🏆"

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

class MenuAction(Enum):
    START = auto()
    QUIT = auto()

class GameResult(Enum):
    WON = auto()
    LOSS = auto()
    QUIT = auto()

class PostGameAction(Enum):
    RESTART = auto()
    MENU = auto()
    QUIT = auto()

class RevealType(Enum):
    ISREVEALED = auto()
    ISFLAGGED = auto()
    ISMINE = auto()

BOARD_DEPTH = 3
TILE_SHAPE = Tile_Shape.SQ
CORNERS = False
RESOLUTION = Resolutions.RES_1080
TACOS = 0
