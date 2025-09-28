import sys
import copy

import cursor
from game_settings import load_settings, update_setting, save_settings
from board import Board
from mines import MineField
from render_menu import RenderMenuCLI
from render_board import RenderBoardCLI
from solver import solver
from config import (
    TileShape,
    TextColor,
    SymbolIcon,
    Resolutions,
    Menu,
    MenuAction,
    GameResult,
    PostGameAction,
    RevealType,
)

settings = load_settings()

def handle_first_load(settings):
    if settings["FIRST_LOAD"] == True:
        invalid = False
        user_input = ""

        while True:
            sys.stdout.write("\033[2J\033[H")
            cursor.print_w_flush("\nThanks for trying Bomb-Boinger!\n") # row 3
            cursor.print_w_flush(f'This is your first time loading, Resolution scale is set to {settings["RESOLUTION"].value}')
            cursor.print_w_flush("Would you like to update Resolution scale?") # row 6
            cursor.input_invalid(invalid, user_input)
            invalid = False

            user_input = input("Y/N: ").strip().upper()
            
            if user_input == "Y":
                res_input = ""

                while True:
                    sys.stdout.write("\033[2J\033[H")
                    cursor.print_w_flush("Choose Resolution:")
                    cursor.print_w_flush('"1" = 480p    "4" = 1080p')
                    cursor.print_w_flush('"2" = 720p    "5" = 2K')
                    cursor.print_w_flush('"3" = 900p    "6" = 4K') #row 8
                    cursor.input_invalid(invalid, res_input)

                    res_input = input("Select option: ").strip().upper()

                    if res_input == "1":
                        update_setting("RESOLUTION", Resolutions.RES_480, settings)
                    elif res_input == "2":
                        update_setting("RESOLUTION", Resolutions.RES_720, settings)
                    elif res_input == "3":
                        update_setting("RESOLUTION", Resolutions.RES_900, settings)
                    elif res_input == "4":
                        update_setting("RESOLUTION", Resolutions.RES_1080, settings)
                    elif res_input == "5":
                        update_setting("RESOLUTION", Resolutions.RES_2K, settings)
                    elif res_input == "6":
                        update_setting("RESOLUTION", Resolutions.RES_4K, settings)                     
                    else:
                        invalid = True
                        continue
                    break

            elif user_input == "N":
                break
            else:
                invalid = True
                continue
        
        update_setting("FIRST_LOAD", False, settings)

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
    user_input = ""
    
    while True:
        sys.stdout.write("\033[2J\033[H")
        menu.draw_menu()

        if invalid:
            if invalid_range:
                cursor.input_invalid(invalid, user_input, "range", width=menu.width)
                invalid_range = False
            elif invalid_locked:
                cursor.input_invalid(invalid, user_input, "locked")
                invalid_locked = False
            else:
                cursor.input_invalid(invalid, user_input)
            invalid = False
        else:
            cursor.input_valid(valid, user_input)
            valid = False

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

                        if 2 <= value <= (menu.width - 2) // 3:
                            update_setting("BOARD_DEPTH", value, settings)
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
                        update_setting("TILE_SHAPE", TileShape.SQ, settings)
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
                    elif user_input == "C":
                        if settings["CORNERS"]:
                            update_setting("CORNERS", False, settings)
                        else:
                            update_setting("CORNERS", True, settings)
                    elif user_input == "F":
                        if settings["AUTO_BACK"]:
                            update_setting("AUTO_BACK", False, settings)
                        else:
                            update_setting("AUTO_BACK", True, settings)
                    else:
                        invalid = True
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
                        update_setting("RESOLUTION", Resolutions.RES_480, settings)
                    elif user_input == "2":
                        update_setting("RESOLUTION", Resolutions.RES_720, settings)                       
                    elif user_input == "3":
                        update_setting("RESOLUTION", Resolutions.RES_900, settings)
                    elif user_input == "4":
                        update_setting("RESOLUTION", Resolutions.RES_1080, settings)
                    elif user_input == "5":
                        update_setting("RESOLUTION", Resolutions.RES_2K, settings)                       
                    elif user_input == "6":
                        update_setting("RESOLUTION", Resolutions.RES_4K, settings)                                            
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
    invalid = False
    user_input = ""

    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]
        tile.reveal_tile(loss=True)
    
    while True:
        sys.stdout.write("\033[2J\033[H")
        render.draw_board()
        cursor.print_w_flush(f'{TextColor.RED.value}BOOM! You exploded.{TextColor.RESET.value}')
        cursor.print_w_flush('Please input "R" for Restart, "M" for Menu, or "Q" for Quit')
        cursor.input_invalid(invalid, user_input)
        invalid = False

        user_input = input("Select option:").strip().upper()

        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M":
            return PostGameAction.MENU
        elif user_input == "R":
            return PostGameAction.RESTART
        else:
            invalid = True
            continue

def flood_reveal(tile, visited=None):
    if visited is None:
        visited = set()

    if tile in visited:
        return
    visited.add(tile)

    if not tile.is_revealed and not tile.is_flagged and not tile.is_mine:

        tile.reveal_tile()

    if tile.adjacent_mines == 0:
        for neighbor in tile.neighbors:
            flood_reveal(neighbor, visited)

def game_won(settings, board):
    render = board.board_render
    invalid = False
    user_input = ""
    
    while True:
        sys.stdout.write("\033[2J\033[H")
        render.draw_board()
        cursor.reset_line()
        cursor.print_w_flush(f'{SymbolIcon.TROPHY.value}Congratulations, You boinged all the Bombs!{SymbolIcon.TROPHY.value}')
        cursor.reset_line()
        cursor.print_w_flush(f'+1 {SymbolIcon.TACO.value}')
        if not invalid:
            update_setting("TACOS", settings["TACOS"] + 1, settings)
        cursor.reset_line()
        cursor.print_w_flush(f'Total {SymbolIcon.TACO.value} accrued: {SymbolIcon.TACO.value * settings["TACOS"]}')
        cursor.reset_line()
        cursor.print_w_flush('Input "M" for Menu, or "Q" for Quit')
        cursor.input_invalid(invalid, user_input)
        invalid = False

        user_input = input("Select option:").strip().upper()
        
        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M" or user_input == "B":
            return PostGameAction.MENU
        else:
            invalid = True
            continue

def check_win_state(board):
    correct_mines = 0
    correct_reveal = 0

    for tile in board.tiles.values():
        if tile.is_mine and tile.is_flagged:
            correct_mines += 1
        if not tile.is_mine and tile.is_revealed:
            correct_reveal += 1

    return (
        correct_mines == len(board.mine_field.mines) and
        correct_reveal == len(board.tiles) - len(board.mine_field.mines)
    )

def start_game(settings, saved_mines, first_reveal_indices):
    
    while True:
        board = Board(settings)
        board.mine_field = MineField(board)

        if saved_mines != None:
            board.mine_field.mines = saved_mines
        else:
            board.mine_field.mines = board.mine_field.generate_mine_indices(board.tile_quantity)

        board.populate_tiles_data()
        board.board_render = RenderBoardCLI(board)

        if saved_mines != None:
            for i in first_reveal_indices:
                board.tiles[i].reveal_tile()
        else:
            first_reveal_indices = board.board_render.first_tile_reveal()

        test_board = copy.deepcopy(board)
        passed = solver(test_board)
        if passed:
            break
        else:
            cursor.print_w_flush("Board did not pass deduction check!")
            continue

    board.mine_field.set_remaining_mines()
    
    game_result = game_load(board)

    return game_result, board.mine_field.mines, first_reveal_indices, board

def game_load(board):
    render = board.board_render
    invalid = False
    invalid_reveal = False
    invalid_flag = False
    invalid_coords = False
    invalid_state = False
    valid = False
    valid_flag = False
    valid_unflag = False
    valid_reveal = False
    valid_move = False
    select_tile_not_action = True
    user_input = ""
    pos = None

    while True:    
        sys.stdout.write("\033[2J\033[H")
        render.draw_board()

        if check_win_state(board):
            return GameResult.WIN

        if invalid:
            if invalid_reveal:
                cursor.input_invalid(invalid, pos, "reveal")
                invalid_reveal = False
            elif invalid_flag:
                cursor.input_invalid(invalid, pos, "flag")
                invalid_locked = False
            elif invalid_coords:
                cursor.input_invalid(invalid, pos, "coords", depth=board.depth)
                invalid_coords = False
            elif invalid_state:
                cursor.input_invalid(invalid, user_input, "state")
                invalid_state = False
            else:
                cursor.input_invalid(invalid, user_input)
            invalid = False
        else:
            if valid_flag:
                cursor.input_valid(valid, pos, "flag")
                valid_flag = False
            elif valid_unflag:
                cursor.input_valid(valid, pos, "unflag")
                valid_unflag = False
            elif valid_reveal:
                cursor.input_valid(valid, pos, "reveal")
                valid_reveal = False
            elif valid_move:
                cursor.input_valid(valid, pos, "move")
                valid_move = False
            else:
                cursor.input_valid(valid, user_input)
            valid = False

        if select_tile_not_action:
            cursor.print_default_board_option()
            user_input = input("Select Option: ").strip().upper()
            pos = cursor.parse_tile_input(user_input)
        
            if user_input == "Q":
                return GameResult.QUIT
            
            elif pos is not None:
                r, c = pos
                tile = board.get_tile_from_coords(pos)

                if tile.is_revealed:
                    invalid = True
                    invalid_reveal = True
                elif 1 <= r <= board.depth and 1 <= c <= board.depth:
                    select_tile_not_action = False
                    valid = True
                    valid_move = True
                else:
                    invalid = True
                    invalid_coords = True               
            else:
                invalid = True
                invalid_state = True
            continue

        else:
            cursor.print_tile_options()
            user_input = input("Select Option: ").strip().upper()

            if user_input == "B":
                select_tile_not_action = True
            elif user_input == "F":
                flag = tile.flag_tile()

                if settings["AUTO_BACK"]:
                    select_tile_not_action = True

                if flag == RevealType.ISREVEALED:
                    invalid = True
                    invalid_reveal = True
                elif flag == RevealType.UNFLAG:
                    valid = True
                    valid_unflag = True
                elif flag == RevealType.ISFLAGGED:
                    valid = True
                    valid_flag = True

            elif user_input == "R":
                reveal = tile.reveal_tile()

                if reveal == RevealType.ISREVEALED:
                    invalid = True
                    invalid_reveal = True
                elif reveal == RevealType.ISFLAGGED:
                    invalid = True
                    invalid_flag = True
                elif reveal == RevealType.ISMINE:
                    return GameResult.LOSS
                else:
                    flood_reveal(tile)
                    valid = True
                    valid_reveal = True
                    select_tile_not_action = True
            else:
                invalid = True
            continue

def main(settings):
 
    handle_first_load(settings)
    
    saved_mines = None
    first_reveal_indices = None

    while True:
        menu_action = menu_load(settings)

        if menu_action == MenuAction.START:

            while True:
                game_result, saved_mines, first_reveal_indices, board = start_game(settings, saved_mines, first_reveal_indices)

                if game_result == GameResult.QUIT:
                    saved_mines = None
                    first_reveal_indices = None
                    break
                elif game_result == GameResult.WIN:
                    post_game_action = game_won(settings, board)
                elif game_result == GameResult.LOSS:
                    post_game_action = game_over(board)

                if post_game_action == PostGameAction.RESTART:
                    continue
                elif post_game_action == PostGameAction.MENU:
                    saved_mines = None
                    first_reveal_indices = None
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