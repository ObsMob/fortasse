import sys

import cursor
from game_settings import load_settings, update_setting, save_settings
from board import Board
from mines import MineField
from render_menu import RenderMenuCLI
from render_board import RenderBoardCLI
from config import (
    TileShape,
    SymbolIcon,
    Resolutions,
    Menu,
    MenuAction,
    GameResult,
    PostGameAction,
    RevealType,
)

settings = load_settings()

def handle_first_load():
    if settings["FIRST_LOAD"] == True:
        invalid = False
        user_input = None

        while True:
            sys.stdout.write("\033[2J\033[H")
            cursor.print_w_flush("\nThanks for trying Bomb-Boinger!\n") # row 3
            cursor.print_w_flush(f'This is your first time loading, Resolution scale is set to {settings["RESOLUTION"].value}')
            cursor.print_w_flush("Would you like to update Resolution scale?\n") # row 6
            if user_input is not None:
                cursor.input_invalid(invalid, user_input)

            user_input = input("Y/N: ").strip().upper()
            
            if user_input == "Y":
                res_input = None

                while True:
                    sys.stdout.write("\033[2J\033[H")
                    cursor.print_w_flush("Choose Resolution:")
                    cursor.print_w_flush('"1" = 480p    "4" = 1080p')
                    cursor.print_w_flush('"2" = 720p    "5" = 2K')
                    cursor.print_w_flush('"3" = 900p    "6" = 4K') #row 8
                    if res_input is not None:
                        cursor.input_invalid(invalid, res_input)

                    res_input = input("Select option: ").strip().upper()

                    if res_input == "1":
                        update_setting("RESOLUTION", Resolutions.RES_480)
                    elif res_input == "2":
                        update_setting("RESOLUTION", Resolutions.RES_720)
                    elif res_input == "3":
                        update_setting("RESOLUTION", Resolutions.RES_900)
                    elif res_input == "4":
                        update_setting("RESOLUTION", Resolutions.RES_1080)
                    elif res_input == "5":
                        update_setting("RESOLUTION", Resolutions.RES_2K)
                    elif res_input == "6":
                        update_setting("RESOLUTION", Resolutions.RES_4K)                     
                    else:
                        invalid = True
                        continue
                    break

            elif user_input == "N":
                break
            else:
                invalid = True
                continue
        
        update_setting("FIRST_LOAD", False)

def quit_game():
    sys.stdout.write("\033[2J\033[H")
    cursor.print_w_flush("\nThanks for Boinging those Bombs!\n")
    sys.exit(0)

def menu_load(settings):
    menu = RenderMenuCLI(settings)
    valid = False
    invalid = False
    invalid_range = False
    invalid_locked = False
    user_input = None
    
    while True:
        sys.stdout.write("\033[2J\033[H")
        menu.draw_menu()

        if user_input is not None:
            if invalid:
                if invalid_range:
                    cursor.input_invalid(invalid, user_input, "range", width=menu.width)
                    invalid_range = False
                elif invalid_locked:
                    cursor.input_invalid(invalid, user_input, "locked")
                    invalid_locked = False
                else:
                    cursor.input_invalid(invalid, user_input)
            else:
                cursor.input_valid(valid, user_input)


        match menu.options_menu:
            
            case Menu.MAIN:
                while True:
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "S":
                        return MenuAction.START
                    elif user_input == "E":
                        menu.options_menu = Menu.EDIT
                    elif user_input == "Q":
                        return MenuAction.QUIT
                    else:
                        invalid = True
                    break
                continue

            case Menu.EDIT:
                while True:
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.MAIN
                    elif user_input == "S":
                        menu.options_menu = Menu.DEPTH
                    elif user_input == "T":
                        menu.options_menu = Menu.TILE
                    elif user_input == "C":
                        menu.options_menu = Menu.CORNERS
                    elif user_input == "R":
                        menu.options_menu = Menu.RES  
                    else:
                        invalid = True
                    break               
                continue

            case Menu.DEPTH:
                while True:
                    user_input = input("Select Option: ").strip().upper()
                    
                    if user_input == "B":
                        menu.options_menu = Menu.EDIT
                        break
                    elif user_input.isdigit():
                        value = int(user_input)

                        if 2 <= value <= menu.width - 2:
                            update_setting("BOARD_DEPTH", value)
                        else:
                            invalid = True
                            invalid_range = True
                            break
                    else:
                        invalid = True
                        break
                    menu.populate_parameters()
                    valid = True                        
                    break
                continue

            case Menu.TILE:
                while True:                  
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.EDIT
                        break
                    elif user_input == "T":
                        invalid = True
                        invalid_locked = True
                        break
                    elif user_input == "S":
                        update_setting("TILE_SHAPE", TileShape.SQ)
                    elif user_input == "H":
                        invalid = True
                        invalid_locked = True
                        break
                    else:
                        invalid = True
                        break
                    menu.populate_parameters()
                    valid = True
                    break
                continue

            case Menu.CORNERS:
                while True:                   
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.EDIT
                        break 
                    elif user_input == "0":
                        update_setting("CORNERS", False)
                    elif user_input == "1":
                        invalid = True
                        invalid_locked = True
                        break
                    else:
                        invalid = True
                        break
                    menu.populate_parameters()
                    valid = True
                    break
                continue

            case Menu.RES:
                while True:                 
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.EDIT
                        break
                    if user_input == "1":
                        update_setting("RESOLUTION", Resolutions.RES_480)
                    elif user_input == "2":
                        update_setting("RESOLUTION", Resolutions.RES_720)                       
                    elif user_input == "3":
                        update_setting("RESOLUTION", Resolutions.RES_900)
                    elif user_input == "4":
                        update_setting("RESOLUTION", Resolutions.RES_1080)
                    elif user_input == "5":
                        update_setting("RESOLUTION", Resolutions.RES_2K)                       
                    elif user_input == "6":
                        update_setting("RESOLUTION", Resolutions.RES_4K)                                            
                    else:
                        invalid = True
                        break
                    menu.update_width()
                    menu.update_width_references()
                    menu.populate_parameters()
                    valid = True
                    break
                continue

def game_over(board):
    render = board.board_render
    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]

        tile.reveal_tile(loss=True)
        render.update_tile_symbol(tile)
        render.draw_tile(tile)
    
    cursor.move_cursor(board.depth * 2 + 5, 0)
    cursor.reset_line()
    cursor.print_w_flush("BOOM! You exploded.")
    cursor.print_w_flush('Please input "R" for Restart, "M" for Menu, or "Q" for Quit\n')

    prompt_row = (board.depth * 2 + 8)

    while True:
        user_input = input("Select option:").strip().upper()

        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M":
            return PostGameAction.MENU
        elif user_input == "R":
            return PostGameAction.RESTART
        else:
            cursor.input_invalid(user_input, prompt_row)

def flood_reveal(tile, board_render, visited=None):
    if visited is None:
        visited = set()

    if tile in visited:
        return
    visited.add(tile)

    if not tile.is_revealed and not tile.is_flagged and not tile.is_mine:

        tile.reveal_tile()
        board_render.update_tile_symbol(tile)
        board_render.draw_tile(tile)

    if tile.adjacent_mines == 0:
        for neighbor in tile.neighbors:
            flood_reveal(neighbor, board_render, visited)

def game_won(settings):
    prompt_row = board.depth * 2 + 10
    cursor.move_cursor(board.depth * 2 + 5, 0)
    cursor.reset_line()
    cursor.print_w_flush(f'{SymbolIcon.TROPHY}Congratulations, You boinged all the Bombs!{SymbolIcon.TROPHY}')
    cursor.reset_line()
    cursor.print_w_flush(f'+1 {SymbolIcon.TACO}')
    update_setting("TACOS", settings["TACOS"] + 1)
    cursor.print_w_flush(f'Total {SymbolIcon.TACO} accrued: {SymbolIcon.TACO * settings["TACOS"]}')
    cursor.print_w_flush('Input "M" for Menu, or "Q" for Quit\n')
    
    while True:
        user_input = input("Select option:").strip().upper()
        
        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M":
            return PostGameAction.MENU
        else:
            cursor.input_invalid(user_input, prompt_row)

def start_game(saved_mines, settings):
    board = Board(settings)
    board.mine_field = MineField(board)

    if saved_mines == None:
        board.mine_field.mines = board.mine_field.generate_mine_indices(board.tile_quantity)
    else:
        board.mine_field.mines = saved_mines

    board.mine_field.set_remaining_mines()
    board.populate_tiles_data()

    game_result = game_load(board)

    return game_result, board.mine_field.mines

def game_load(board):
    cursor.move_cursor()
    board.board_render = RenderBoardCLI(board)
    render = board.board_render
    sys.stdout.write("\033[2J\033[H")
    render.draw_board()
    render.draw_remaining_mines()
    render.first_tile_reveal()

    prompt_row = board.depth * 2 + 6

    while True:

        if board.mine_field.remaining_mines == 0:
            correct_mines = 0

            for tile in board.tiles:
                if tile.is_mine and tile.is_flagged:
                    correct_mines += 1

            if correct_mines == len(board.mine_field.mines):
                return GameResult.WIN

        cursor.print_default_board_option(prompt_row)
        raw = input("Select Option: ").strip().upper()
        pos = cursor.parse_tile_input(raw)
        
        if raw == "Q":
            return GameResult.QUIT
        
        elif pos is not None:
            r, c = pos

            if 1 <= r <= board.depth and 1 <= c <= board.depth:
                while True:
                    
                    cursor.print_tile_options(prompt_row)
                    action = input("Select Option: ").strip().upper()

                    if action == "B":
                        break
                    if action == "F":
                        tile = board.get_tile_from_coords(pos)
                        flag = tile.flag_tile()

                        if flag == RevealType.ISREVEALED:
                            cursor.input_invalid(pos, prompt_row, "reveal")
                        else:
                            render.update_tile_symbol(tile)
                            render.draw_tile(tile)
                            render.draw_remaining_mines()
                            break

                    if action == "R":
                        tile = board.get_tile_from_coords(pos)
                        reveal = tile.reveal_tile()

                        if reveal == RevealType.ISREVEALED:
                            cursor.input_invalid(pos, prompt_row, "reveal")
                        elif reveal == RevealType.ISFLAGGED:
                            cursor.input_invalid(pos, prompt_row, "flag")
                        elif reveal == RevealType.ISMINE:
                            return GameResult.LOSS
                        else:
                            render.update_tile_symbol(tile)
                            render.draw_tile(tile)
                            flood_reveal(tile, render)
                            break
            else:
                cursor.input_invalid(pos, prompt_row, "coords", depth=board.depth)
            
        else:
            cursor.input_invalid(raw, prompt_row, "state")

def main(settings):
 
    handle_first_load()
    
    saved_mines = None

    while True:
        menu_action = menu_load(settings)

        if menu_action == MenuAction.START:

            while True:
                game_result, saved_mines = start_game(saved_mines, settings)

                if game_result == GameResult.QUIT:
                    break
                elif game_result == GameResult.WON:
                    post_game_action = game_won(settings)
                elif game_result == GameResult.LOSS:
                    post_game_action = game_over()

                if post_game_action == PostGameAction.RESTART:
                    continue
                elif post_game_action == PostGameAction.MENU:
                    saved_mines = None
                    break
                elif post_game_action == PostGameAction.QUIT:
                    save_settings(settings)
                    return quit_game()

        elif menu_action == MenuAction.QUIT:
            break

    save_settings(settings)
    quit_game()


if __name__ == "__main__":
    main(settings)