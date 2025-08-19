import math
import rand
import sys

from config import FIRST_LOAD, RESOLUTION, TILE_SHAPE, Tile_Shape
from board import Board
from render_mednu import RenderMenuCLI



def main():
    prompt_row = 7
    prompt_column = 1

    handle_first_load()
    menu_load()

    board = Board()
    render = board.board_render


def ansi_move_cursor(row=1, column=1):
    move_cursor = f'\033[{row};{column}H'
    print(move_cursor, end="", flush=True)

def ansi_default_cursor():
    ansi_move_cursor(prompt_row, 15)

def ansi_reset_line():
    ANSI_reset = "\033[K"
    print(ANSI_reset, end="", flush=True)

def input_invalid(arg, usage=None):
    ansi_move_cursor(prompt_row - 1, prompt_column)
    ansi_reset_line()
    if usage == None:
        print(f'Invalid Selection "{arg}". Please try again.', end="", flush=True)
    elif usage == "locked":
        print(f'Invalid Selection "{arg}. Currently Locked. Check back next update.', end="", flush=True)
    elif usage == "state_index"
        print(f'Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2', end="", flush=True)
    elif usage == "range":
        print(f'Invalid Range "{arg}". Must be between 2 and {menu.width - 2}', end="", flush=True)
    ansi_default_cursor()

def input_valid(arg):
    ansi_move_cursor(prompt_row - 1, prompt_column)
    ansi_reset_line()
    print(f'Input {arg} accepted!', end="", flush=True)
    ansi_default_cursor()

def game_over(board):
    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]

        tile.reveal_tile(loss=True)
        board.board_render.update_tile_symbol(tile)
    
    ansi_move_cursor(board.depth * 2 + 2, 0)
    ansi_reset_line()
    print("\nBOOM! You exploded.\n")
    print('Please input "R" for Restart, "M" for Menu, or "Q" for Quit\n')

    while True:
        user_input = input("Select option:").strip().upper()

        if user_input == "R":
            #Reset using same board
            break
        if user_input == "M":
            menu_load()
            break
        if user_input == "Q":
            quit_game()
            break
            
def first_open_tile(board):
    extra_safe_tiles = set()
    kinda_safe_tiles = set()

    for i, tile in board.tiles.items():
        if tile.adjacent_mines == 0:
            extra_safe_tiles.add(i)

    if len(extra_safe_tiles) > 0: 
        start_tile_index = extra_safe_tiles[random.choice(len(extra_safe_tiles))]
        start_tile = board.tiles[start_tile_index]

        start_tile.reveal_tile()
        render.update_tile_symbol(start_tile)
        print(f'\nTile {start_tile.index} at {start_tile.coords} has been revealed!\n')
        return 

    else:
        for i, tile in board.tiles.items():
            if tile.adjacent_mines <= 2:
                kinda_safe_tiles.add(i)
        
        three_or_less = min(3, len(kinda_safe_tiles))
        start_tiles_indices = random.sample(kinda_safe_tiles, three_or_less)

        for i in start_tiles_indices:
            start_tile = board.tiles[i]
            
            start_tile.reveal_tile()
            render.update_tile_symbol(start_tile)
            print(f'\nTile {start_tile.index} at {start_tile.coords} has been revealed!\n')

def handle_first_load():
    if FIRST_LOAD:
        print("\nThanks for trying Bomb-Boinger!\n") # row 3
        print("This is your first time loading, default Resolution scale is set to 1080p")
        print("Would you like to update Resolution scale?\n") # row 6
        
        while True:
            user_input = input("Y/N: ").strip().upper()

            if user_input == "Y":
                ansi_reset_line()
                prompt_row = 4
                ansi_move_cursor(prompt_row)
                print("Choose Resolution:")
                print('"1" = 1080')
                print('"2" = 2K')
                print('"3" = 4K\n') #row 8
                
                while True:
                    res_input = input("Select option: ").strip()

                    if res_input == "1":
                        break
                    elif res_input == "2":
                        config.RESOLUTION = Resolutions.RES_2K
                        break
                    elif res_input == "3":
                        config.RESOLUTION = Resolutions.RES_4K
                        break
                    else:
                        input_invalid(res_input)
                        ansi_default_cursor()
                break

            elif user_input == "N":
                break
            else:
                input_invalid(user_input)
                ansi_move_cursor(7, 5)
        
        config.FIRST_LOAD = False

def menu_load():
    ansi_move_cursor()
    menu = RenderMenuCLI()
    menu.draw_menu
    prompt_row = 24
    
    while True:
        match menu.options_menu:
            
            case Menu.MAIN:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "S":
                        start_game()
                        break
                    elif user_input == "E":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "Q":
                        quit_game()
                        break
                    else:
                        input_invalid(user_input)

            case Menu.EDIT:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "S":
                        menu.options_menu = Menu.DEPTH
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "T":
                        menu.options_menu = Menu.TILE
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "C":
                        menu.options_menu = Menu.CORNERS
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "R":
                        menu.options_menu = Menu.RES
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.MAIN
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input)

            case Menu.DEPTH:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()
                    user_input = input("Select Option: ").strip().upper()
                    
                    if user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break
                    elif user_input.isdigit():
                        value = int(user_input)
                            if 2 <= value <= menu.width - 2:
                                config.BOARD_DEPTH = value
                                menu.draw_new_parameter()
                                break
                            else:
                                input_invalid(user_input, "range")
                    else:
                        input_invalid(user_input)

            case Menu.TILE:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "T":
                        input_invalid(user_input, "locked")
                        break
                    elif user_input == "S":
                        config.TILE_SHAPE = Tile_Shape.SQ
                        menu.draw_new_parameter()
                        input_valid(user_input)
                        break
                    elif user_input == "H":
                        input_invalid(user_input, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input)

            case Menu.CORNERS:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "0":
                        config.CORNERS = False
                        menu.draw_new_parameter()
                        input_valid(user_input)
                    elif user_input == "1":
                        input_invalid(user_input, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input)

            case Menu.RES:
                while True:
                    ansi_default_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "1":
                        config.RESOLUTION = Resolutions.RES_1080
                        menu.draw_new_parameter()
                        input_valid(user_input)
                        break
                    elif user_input == "2":
                        config.RESOLUTION = Resolutions.RES_2K
                        menu.draw_new_parameter()
                        input_valid(user_input)
                        break
                    elif user_input == "3":
                        config.RESOLUTION = Resolutions.RES_4K
                        menu.draw_new_parameter()
                        input_valid(user_input)                        
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input)


def quit_game():
    sys.standout.write("\033[2J\033[H")
    print("\nThanks for Boinging those Bombs!\n")
    sys.exit(0)














if __name__ == "__main__":
    main()