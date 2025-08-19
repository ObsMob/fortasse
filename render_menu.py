from config import (
    TILE_WIDTH,
    BOARD_DEPTH,
    TILE_SHAPE,
    CORNERS,
    RESOLUTION,
    Resolutions,
    Menu,
)

class RenderMenuCLI():
    def __init__(self):
        self.options_menu = Menu.MAIN 
        self.width = 50

        greeting = "Welcome to Bomb-Boinger!"
        parameters_header = "Current Parameters"
        options_header = "Input Options. Press:"
        prompt_lock = '(Currently locked. Soon™)'
        parameters =[
            f'Board Size = {BOARD_DEPTH}',              # ANSI(8, 14) r, c (including outline)
            f'Tile Shape = {TILE_SHAPE.value} {prompt_lock}', # ANSI(9, 14)
            f'Corners Touch = {CORNERS} {prompt_lock}', # ANSI(10, 17)
            f'Current Resolution = {RESOLUTION.value}'  # ANSI(11, 22)
        ]
        options_sections = {
            "main_options": [
                '"S" = Start Game',                     # ANSI(16, 2) r, c (including outline)                     
                '"E" = Edit Parameters',                # ANSI(17, 2)
                '"Q" = Quit Game'                       # ANSI(18, 2)
            ],
            "edit_options": [
                '"S" = Board Size',                     # ANSI(16, 2) r, c (including outline) 
                '"T" = Tile Shape',                     # ANSI(17, 2)
                '"C" = Corners',                        # ANSI(18, 2)
                '"R" = Resolution',                     # ANSI(19, 2)
                '"B" = Back to Main Menu'               # ANSI(20, 2)
            ],
            "board_prompt": [
                f'Enter Integer: 2-{self.width - 2}',   # ANSI(16, 2) r, c (including outline)
                '"B" = Back to Edit Menu'               # ANSI(17, 2)
            ],
            "tile_prompt": [
                '"T" = Triangle - LOCKED',              # ANSI(16, 2) r, c (including outline) 
                '"S" = Square',                         # ANSI(17, 2)
                '"H" = Hexagon - LOCKED',               # ANSI(18, 2)
                '"B" = Back to Edit Menu'               # ANSI(19, 2)
            ],
            "corner_prompt": [
                '"0" = False',                          # ANSI(16, 2) r, c (including outline) 
                '"1" = True - LOCKED',                  # ANSI(17, 2)
                '"B" = Back to Edit Menu'               # ANSI(18, 2)
            ],
            "resolution_prompt": [
                '"1" = 1080',                           # ANSI(16, 2) r, c (including outline) 
                '"2" = 2K',                             # ANSI(17, 2)
                '"3" = 4K',                             # ANSI(18, 2)
                '"B" = Back to Edit Menu'               # ANSI(19, 2)
            ]
        }
        max_options_rows = max(len(options_list) for options_list in menu.options_sections.values())

    def draw_menu(self):
        header_text = ""
        option_text = ""

        top = f'{Symbol_Icon.TOPLEFT}{Symbol_Icon.HORIZ * self.width}{Symbol_Icon.TOPRIGHT}'
        bottom = f'{Symbol_Icon.BOTLEFT}{Symbol_Icon.HORIZ * self.width}{Symbol_Icon.BOTRIGHT}'
        divider = f'{Symbol_Icon.LEFTTEE}{Symbol_Icon.HORIZ * self.width}{Symbol_Icon.RIGHTTEE}'
        header = f'{Symbol_Icon.VERT}{header_text:^{self.width}}{Symbol_Icon.VERT}'
        option = f'{Symbol_Icon.VERT}{option_text}{Symbol_Icon.EMPTY * self.width - len(option_text)}{Symbol_Icon.VERT}'
        empty_row = f'{Symbol_Icon.VERT}{Symbol_Icon.EMPTY * self.width}{Symbol_Icon.VERT}'

        match RESOLUTION:
            # case Resolutions.RES_480:
            #     self.width = round(self.width * .48)
            # case Resolutions.RES_720:
            #     self.width = round(self.width * .66)
            # case Resolutions.RES_900:
            #     self.width = round(self.width * .83)
            case Resolutions.RES_1080:
                pass
            case Resolutions.RES_2K:
                self.width = round(self.width * 1.33)
            case Resolutions.RES_4K:
                self.width = round(self.width * 2)
        
        self.greeting_section()
        self.parameter_section()
        self.initial_options_section()

    def greeting_section(self):
        header_text = greeting
        
        print(top)
        print(empty_row)
        print(header)
        print(empty_row)
        print(divider) 

    def parameter_section(self):
        header_text = parameters_header

        print(header)
        print(empty_row)
        for i in range(len(parameters)):
            option_text = parameters[i]
            print(option)
        print(empty_row)
        print(divider)
        # Row 13

    def initial_options_section(self):
        header_text = options_header
        filler_rows = max_options_rows - len(options_sections[main_options])
        
        print(header)
        print(empty_row)
        # Row 15
        for option_value in options_sections[main_options]:
            option_text = option_value
            print(option)
        for i in range(filler_lines):
            print(empty_row)
        print(empty_row)
        print(bottom)
        # Row 22

    def draw_new_parameter(self):
        ANSI_row = 0
        ANSI_column = 0
        updated_text = ""
        ANSI_update = f'\033[{ANSI_row};{ANSI_column}H{updated_text}:<{self.width - ANSI_column}'

        match self.options_menu:
            case Menu.DEPTH:
                ANSI_row = 8
                ANSI_column = 14
                updated_text = BOARD_DEPTH
                return print(ANSI_update, end="", flush=True)
            case Menu.TILE:
                ANSI_row = 9
                ANSI_column = 14
                updated_text = TILE_SHAPE.value
                return print(ANSI_update, end="", flush=True)
            case Menu.CORNERS:
                ANSI_row = 10
                ANSI_column = 17
                updated_text = CORNERS
                return print(ANSI_update, end="", flush=True)
            case Menu.RES:
                ANSI_row = 11
                ANSI_column = 22
                updated_text = RESOLUTION.value
                return print(ANSI_update, end="", flush=True)

    def draw_new_option_menu(self):
        ANSI_row = 16
        ANSI_column = 2
        ANSI_update = f'\033[{ANSI_row};{ANSI_column}H{updated_text}:<{self.width}'

        match self.options_menu:
            case Menu.MAIN:
                option_section = "main_options"
            case Menu.EDIT:
                option_section = "edit_options"         
            case Menu.DEPTH:
                option_section = "board_prompt"
            case Menu.TILE:
                option_section = "tile_prompt"
            case Menu.CORNERS:
                option_section = "corner_prompt"
            case Menu.RES:
                option_section = "resolution_prompt"
        
        filler_rows = max_options_rows - len(options_sections[option_section])
        
        for option in options_sections[option_section]:
            updated_text = option
            print(ANSI_update, end="", flush=True)
            ANSI_row += 1
        for row in filler_rows:
            print(empty_row, end="", flush=True)
