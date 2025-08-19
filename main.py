import math
import rand
import sys

import cursor
from board import Board
from render_menu import RenderMenuCLI
from config import (
    FIRST_LOAD, 
    RESOLUTION, 
    TILE_SHAPE, 
    Tile_Shape, 
    MenuAction, 
    GameResult
)



def handle_first_load():
    if FIRST_LOAD:
        print_w_flush("\nThanks for trying Bomb-Boinger!\n") # row 3
        print_w_flush("This is your first time loading, default Resolution scale is set to 1080p")
        print_w_flush("Would you like to update Resolution scale?\n") # row 6
        
        while True:
            prompt_row = 7
            user_input = input("Y/N: ").strip().upper()

            if user_input == "Y":
                
                for r in range (4, 8): # Clearing lines 4-7
                    row = r
                    move_cursor(row)
                    reset_line()

                move_cursor(4)
                print_w_flush("Choose Resolution:")
                print_w_flush('"1" = 1080')
                print_w_flush('"2" = 2K')
                print_w_flush('"3" = 4K\n') #row 8
                
                while True:
                    prompt_row = 9
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
                        input_invalid(res_input, prompt_row)
                break

            elif user_input == "N":
                break
            else:
                input_invalid(user_input, prompt_row)
        
        config.FIRST_LOAD = False

def quit_game():
    sys.standout.write("\033[2J\033[H")
    print_w_flush("\nThanks for Boinging those Bombs!\n")
    sys.exit(0)

def menu_load():
    move_cursor()
    menu = RenderMenuCLI()
    menu.draw_menu
    prompt_row = 24
    
    while True:
        match menu.options_menu:
            
            case Menu.MAIN:
                while True:
                    move_cursor(prompt_row)
                    reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "S":
                        return MenuAction.START
                    elif user_input == "E":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break
                    elif user_input == "Q":
                        return MenuAction.QUIT
                    else:
                        input_invalid(user_input, prompt_row)

            case Menu.EDIT:
                while True:
                    move_cursor(prompt_row)
                    reset_line()                    
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
                        input_invalid(user_input, prompt_row)

            case Menu.DEPTH:
                while True:
                    move_cursor(prompt_row)
                    reset_line()
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
                                input_valid(arg, prompt_row)
                                break
                            else:
                                input_invalid(user_input, prompt_row, "range", menu.width)
                    else:
                        input_invalid(user_input, prompt_row)

            case Menu.TILE:
                while True:
                    move_cursor()
                    reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "T":
                        input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "S":
                        config.TILE_SHAPE = Tile_Shape.SQ
                        menu.draw_new_parameter()
                        input_valid(user_input, prompt_row)
                        break
                    elif user_input == "H":
                        input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input, prompt_row)

            case Menu.CORNERS:
                while True:
                    move_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "0":
                        config.CORNERS = False
                        menu.draw_new_parameter()
                        input_valid(user_input, prompt_row)
                        break
                    elif user_input == "1":
                        input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input, prompt_row)

            case Menu.RES:
                while True:
                    move_cursor()
                    reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "1":
                        config.RESOLUTION = Resolutions.RES_1080
                        menu.draw_new_parameter()
                        input_valid(user_input,prompt_row)
                        break
                    elif user_input == "2":
                        config.RESOLUTION = Resolutions.RES_2K
                        menu.draw_new_parameter()
                        input_valid(user_input,prompt_row)
                        break
                    elif user_input == "3":
                        config.RESOLUTION = Resolutions.RES_4K
                        menu.draw_new_parameter()
                        input_valid(user_input, prompt_row)                        
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        input_invalid(user_input, prompt_row)

def game_over(board):
    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]

        tile.reveal_tile(loss=True)
        board.board_render.update_tile_symbol(tile)
    
    move_cursor(board.depth * 2 + 5, 0)
    reset_line()
    print_w_flush("BOOM! You exploded.")
    print_w_flush('Please input "R" for Restart, "M" for Menu, or "Q" for Quit\n')

    prompt_row = (board.depth * 2 + 8)

    while True:
        user_input = input("Select option:").strip().upper()

        if user_input == "Q":
            return quit_game()
        elif user_input == "M":
            return menu_load()
        elif user_input == "R":
            return start_game(same_game=True)
        else:
            input_invalid(user_input, prompt_row)

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

def start_game(same_game=False):





def main():
    handle_first_load()
    
    saved_mines_list = []
    game_running = True

    while game_running:
        menu_action = menu_load()

        if menu_action == True:
            game_result = start_game()
        elif game_start == False:
            game_running = False

quit_game()

    


if __name__ == "__main__":
    main()