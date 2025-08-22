from cursor import print_w_flush, print_wo_newline
from config import Menu, SymbolIcon, Resolutions


class RenderMenuCLI():
    def __init__(self, settings):
        self.settings = settings
        self.options_menu = Menu.MAIN
        self.arbitrary_base_width_scale = 131
        self.width = 0
        self.greeting = "Welcome to Bomb-Boinger!"
        self.parameters_header = "Current Parameters"
        self.options_header = "Input Options"
        self.prompt_lock = '(Currently locked. Soon™)'
        self.max_options_rows = None

        self.update_width()
        self.update_width_references()
        self.populate_parameters()

    def populate_parameters(self):
        self.parameters =[
            f'Board Size = {self.settings["BOARD_DEPTH"]}x{self.settings["BOARD_DEPTH"]}',
            f'Tile Shape = {self.settings["TILE_SHAPE"].value} {self.prompt_lock}',
            f'Corners Touch = {self.settings["CORNERS"]} {self.prompt_lock}',
            f'"Back" on Flag/Unflag = {self.settings["AUTO_BACK"]} {self.prompt_lock}',
            f'Current Resolution = {self.settings["RESOLUTION"].value}'                     
        ]

    def populate_options_sections(self):
        self.options_sections = {
            "main_options": [
                '"S" = Start Game',                     # ANSI(16, 2) r, c (including outline)                     
                '"E" = Edit Parameters',                # ANSI(17, 2)
                '"Q" = Quit Game'                       # ANSI(18, 2)
            ],
            "edit_options": [
                '"S" = Board Size',
                '"T" = Tile Shape',
                '"C" = Corners and "Auto-Back',
                '"R" = Resolution',
                '"B" = Back to Main Menu'
            ],
            "board_prompt": [
                f'Enter Integer: "2-{(self.width - 2) // 3}"',
                '"B" = Back to Edit Menu'
            ],
            "tile_prompt": [
                '"T" = Triangle - LOCKED',              # ANSI(16, 2) r, c (including outline) 
                '"S" = Square',                         # ANSI(17, 2)
                '"H" = Hexagon - LOCKED',               # ANSI(18, 2)
                '"B" = Back to Edit Menu'               # ANSI(19, 2)
            ],
            "corner_prompt": [
                '"C" = Toggle Corners',
                '"F" = Toggle "Auto-Back" on Flag/Unflag',
                '"B" = Back to Edit Menu'
            ],
            "resolution_prompt": [
                '"1" = 480p        "4" = 1080p',
                '"2" = 720p        "5" = 2K',
                '"3" = 900p        "6" = 4K',
                '"B" = Back to Edit Menu'
            ]
        }

    def update_width(self):
        match self.settings["RESOLUTION"]:
            case Resolutions.RES_480:
                self.width = round(self.arbitrary_base_width_scale * .4444)
            case Resolutions.RES_720:
                self.width = round(self.arbitrary_base_width_scale * .6666)
            case Resolutions.RES_900:
                self.width = round(self.arbitrary_base_width_scale * .8333)
            case Resolutions.RES_1080:
                self.width = self.arbitrary_base_width_scale
            case Resolutions.RES_2K:
                self.width = round(self.arbitrary_base_width_scale * 1.3333)
            case Resolutions.RES_4K:
                self.width = round(self.arbitrary_base_width_scale * 2)

    def update_width_references(self):

        self.populate_options_sections()
        self.max_options_rows = max(len(options_list) for options_list in self.options_sections.values())

    def draw_menu(self):

        self.draw_greeting_section()
        self.draw_parameter_section()
        self.draw_option_section()
        
    def draw_greeting_section(self):
        header_text = self.greeting
        
        self.top_row()
        self.empty_row()
        self.header_row(header_text)
        self.empty_row()
        self.divider_row()
        # Row 5

    def draw_parameter_section(self):
        header_text = self.parameters_header

        self.header_row(header_text)
        self.empty_row()

        for param in self.parameters:
            self.option_row(param)

        self.empty_row()
        self.divider_row()
        # Row 13

    def draw_option_section(self):
        header_text = self.options_header

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

        filler_rows = self.max_options_rows - len(self.options_sections[option_section])
        
        self.header_row(header_text)
        self.empty_row()
        # Row 15
        for option_text in self.options_sections[option_section]:
            self.option_row(option_text)

        for r in range(filler_rows):
            self.empty_row()

        self.empty_row()
        self.bot_row()
        # Row 22

    def top_row(self):
        return print_w_flush(f'{SymbolIcon.TOPLEFT.value}{SymbolIcon.HORIZ.value * self.width}{SymbolIcon.TOPRIGHT.value}')

    def bot_row(self):
        return print_w_flush(f'{SymbolIcon.BOTLEFT.value}{SymbolIcon.HORIZ.value * self.width}{SymbolIcon.BOTRIGHT.value}')
    
    def divider_row(self):
        return print_w_flush(f'{SymbolIcon.LEFTTEE.value}{SymbolIcon.HORIZ.value * self.width}{SymbolIcon.RIGHTTEE.value}')
    
    def option_row(self, option_text):
        return print_w_flush(f'{SymbolIcon.VERT.value}{option_text:<{self.width}}{SymbolIcon.VERT.value}')

    def empty_row(self):
        return print_w_flush(f'{SymbolIcon.VERT.value}{" " * self.width}{SymbolIcon.VERT.value}')

    def header_row(self, header_text):
        return print_w_flush(f'{SymbolIcon.VERT.value}{header_text:^{self.width}}{SymbolIcon.VERT.value}')
