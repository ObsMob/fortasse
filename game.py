import sys
import time

import cursor
from board import Board
from render_board import RenderBoardCLI
from render_holes import cli_holes_render
from solver import solver
from solver_class_copies import SolverBoard
from game_settings import update_setting
from config import (
    GameResult,
    RevealType,
    PostGameAction,
    SymbolIcon,
    TextColor,
)

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
        cursor.reset_line()
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

def game_won(settings, board):
    render = board.board_render
    invalid = False
    user_input = ""
    
    while True:
        sys.stdout.write("\033[2J\033[H")
        render.draw_board()
        cursor.print_w_flush(f'{SymbolIcon.TROPHY.value}Congratulations, You boinged all the Bombs!{SymbolIcon.TROPHY.value}')
        cursor.print_w_flush(f'+1 {SymbolIcon.TACO.value}')
        if not invalid:
            update_setting("TACOS", settings["TACOS"] + 1, settings)
        cursor.print_w_flush(f'Total {SymbolIcon.TACO.value} accrued: {SymbolIcon.TACO.value * settings["TACOS"]}')
        cursor.print_w_flush('Input "M" for Menu, or "Q" for Quit')
        cursor.input_invalid(invalid, user_input)
        invalid = False
        cursor.reset_line()
        user_input = input("Select option:").strip().upper()
        
        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M" or user_input == "B":
            return PostGameAction.MENU
        else:
            invalid = True
            continue

def check_win_state(board):
    correct_flagged = 0
    correct_revealed = 0
    must_clear = board.tile_quantity

    if board.holes:
        must_clear -= len(board.hole_field.holes)

    for tile in board.tiles.values():
        if tile.is_mine and tile.is_flagged:
            correct_flagged += 1
        if not tile.is_mine and not tile.is_hole and tile.is_revealed:
            correct_revealed += 1

    return (
        correct_flagged + correct_revealed == must_clear and
        correct_flagged == len(board.mine_field.mines)
    )

def game_init(restart, settings, board):
    ellipsis = "."
    last_update = 0
    update_interval = 0.3
    
    while True:
        new_board = Board(settings)

        if restart:
            new_board.saved_board_data = board.saved_board_data
            new_board.mine_field.mines = board.saved_board_data[0]
            new_board.hole_field.holes = board.saved_board_data[1]
            new_board.first_reveals = board.saved_board_data[2]

        else:
            new_board.mine_field.generate_mine_indices()
            if new_board.holes:
                new_board.hole_field.generate_hole_indices()

        new_board.populate_tiles_data()
        new_board.mine_field.set_remaining_mines()
        new_board.board_render = RenderBoardCLI(new_board)

        if not restart:
            new_board.populate_first_reveals()
            new_board.populate_save_data()

        for i in new_board.first_reveals:
            tile = new_board.tiles[i]
            tile.reveal_tile()
            new_board.board_render.update_tile_symbol(tile)
                
        if new_board.holes:
            cli_holes_render(new_board)
            
        test_board = SolverBoard(new_board)
        passed = solver(test_board)
        if passed:
            cursor.print_w_flush("")
            cursor.print_w_flush("Board Check Passed!")
            break
        else:
            now = time.time()
            if now - last_update > update_interval:
                last_update = now
                ellipsis = cursor.deduction_load_wait(ellipsis)
   
    game_result = game_start(new_board, settings)

    return game_result, new_board

def game_start(board, settings):
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
            cursor.reset_line()
            user_input = input("Select Option: ").strip().upper()
            pos = cursor.parse_tile_input(user_input)
        
            if user_input == "Q":
                return GameResult.QUIT
            
            elif pos is not None:
                r, c = pos
                tile = board.get_tile_from_coords(pos)

                if tile != None and tile.is_revealed:
                    invalid = True
                    invalid_reveal = True
                elif tile != None and tile.is_hole:
                    invalid = True
                    invalid_state = True
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
            cursor.reset_line()
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
                    tile.flood_reveal()
                    valid = True
                    valid_reveal = True
                    select_tile_not_action = True
            else:
                invalid = True
            continue
