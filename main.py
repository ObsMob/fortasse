import sys

import cursor
import config
from board import Board
from mines import MineField
from render_menu import RenderMenuCLI
from render_board import RenderBoardCLI


def handle_first_load():
    if config.FIRST_LOAD:
        cursor.print_w_flush("\nThanks for trying Bomb-Boinger!\n") # row 3
        cursor.print_w_flush("This is your first time loading, default Resolution scale is set to 1080p")
        cursor.print_w_flush("Would you like to update Resolution scale?\n") # row 6
        
        while True:
            prompt_row = 7
            user_input = input("Y/N: ").strip().upper()

            if user_input == "Y":
                
                for r in range (4, 8): # Clearing lines 4-7
                    row = r
                    cursor.move_cursor(row)
                    cursor.reset_line()

                cursor.move_cursor(4)
                cursor.print_w_flush("Choose Resolution:")
                cursor.print_w_flush('"1" = 1080')
                cursor.print_w_flush('"2" = 2K')
                cursor.print_w_flush('"3" = 4K\n') #row 8
                
                while True:
                    prompt_row = 9
                    res_input = input("Select option: ").strip()

                    if res_input == "1":
                        break
                    elif res_input == "2":
                        config.RESOLUTION = config.Resolutions.RES_2K
                        break
                    elif res_input == "3":
                        config.RESOLUTION = config.Resolutions.RES_4K
                        break
                    else:
                        cursor.input_invalid(res_input, prompt_row)
                break

            elif user_input == "N":
                break
            else:
                cursor.input_invalid(user_input, prompt_row)
        
        config.FIRST_LOAD = False
        print("DEBUG: FIRST_LOAD =", config.FIRST_LOAD)
        
def quit_game():
    sys.standout.write("\033[2J\033[H")
    cursor.print_w_flush("\nThanks for Boinging those Bombs!\n")
    sys.exit(0)

def menu_load():
    cursor.move_cursor()
    menu = RenderMenuCLI()
    menu.draw_menu
    prompt_row = 24
    
    while True:
        match menu.options_menu:
            
            case config.Menu.MAIN:
                while True:
                    cursor.move_cursor(prompt_row)
                    cursor.reset_line()                    
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
                        cursor.input_invalid(user_input, prompt_row)

            case config.Menu.EDIT:
                while True:
                    cursor.move_cursor(prompt_row)
                    cursor.reset_line()                    
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
                        menu.options_menu = Menu.config.CORNERS
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
                        cursor.input_invalid(user_input, prompt_row)

            case config.Menu.DEPTH:
                while True:
                    cursor.move_cursor(prompt_row)
                    cursor.reset_line()
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
                            cursor.input_valid(arg, prompt_row)
                            break
                        else:
                            cursor.input_invalid(user_input, prompt_row, "range", menu.width)
                    else:
                        cursor.input_invalid(user_input, prompt_row)

            case config.Menu.TILE:
                while True:
                    cursor.move_cursor()
                    cursor.reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "T":
                        cursor.input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "S":
                        config.TILE_SHAPE = config.Tile_Shape.SQ
                        menu.draw_new_parameter()
                        cursor.input_valid(user_input, prompt_row)
                        break
                    elif user_input == "H":
                        cursor.input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        cursor.input_invalid(user_input, prompt_row)

            case config.Menu.CORNERS:
                while True:
                    cursor.move_cursor()
                    ansi_reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "0":
                        config.CORNERS = False
                        menu.draw_new_parameter()
                        cursor.input_valid(user_input, prompt_row)
                        break
                    elif user_input == "1":
                        cursor.input_invalid(user_input, prompt_row, "locked")
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        cursor.input_invalid(user_input, prompt_row)

            case config.Menu.RES:
                while True:
                    cursor.move_cursor()
                    cursor.reset_line()                    
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "1":
                        config.RESOLUTION = config.Resolutions.RES_1080
                        menu.draw_new_parameter()
                        cursor.input_valid(user_input,prompt_row)
                        break
                    elif user_input == "2":
                        config.RESOLUTION = config.Resolutions.RES_2K
                        menu.draw_new_parameter()
                        cursor.input_valid(user_input,prompt_row)
                        break
                    elif user_input == "3":
                        config.RESOLUTION = config.Resolutions.RES_4K
                        menu.draw_new_parameter()
                        cursor.input_valid(user_input, prompt_row)                        
                        break
                    elif user_input == "B":
                        menu.options_menu = Menu.EDIT
                        menu.draw_new_option_menu()
                        break                        
                    else:
                        cursor.input_invalid(user_input, prompt_row)

def game_over(board):
    render = board.board_render
    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]

        tile.reveal_tile(loss=True)
        render.update_tile_symbol(tile)
        render.render_tile(tile)
    
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

def first_open_tile(board):
    render = board.render_board
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
        render.draw_tile(start_tile)
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
            render.draw_tile(start_tile)

def flood_reveal(tile, board_render):
    
    if tile.adjacent_mines == 0:
        for neighbor in tile.neighbors:
            flood_reveal(neighbor, board_render)

    if tile.is_revealed or tile.is_flagged or tile.is_mine:
        return
    
    tile.reveal_tile()
    board_render.update_tile_symbol(tile)
    board_render.draw_tile(tile)

def game_won():
    cursor.move_cursor(board.depth * 2 + 5, 0)
    cursor.reset_line()
    cursor.print_w_flush(f'{Symbol_Icon.TROPHY}Congratulations, You boinged all the Bombs!{Symbol_Icon.TROPHY}')
    cursor.reset_line()
    cursor.print_w_flush(f'+1 {Symbol_Icon.TACO}')
    TACOS += 1
    cursor.print_w_flush(f'Total {Symbol_Icon.TACO} accrued: {Symbol_Icon.TACO * TACOS}')
    cursor.print_w_flush('Input "M" for Menu, or "Q" for Quit\n')
    
    while True:
        user_input = input("Select option:").strip().upper()
        
        if user_input == "Q":
            return PostGameAction.QUIT
        elif user_input == "M":
            return PostGameAction.MENU
        else:
            cursor.input_invalid(user_input, prompt_row)

def start_game(saved_mines):
    board = Board()
    board.mine_field = MineField(board)

    if saved_mines == None:
        board.mine_field.mines = board.mine_field.generate_mine_indices(board.tile_quantity)
    else:
        board.mine_field.mines = saved_mines

    board.mine_field.update_remaining_mines()
    board.populate_tiles_data()

    game_result = game_load(board)

    return game_result, board.mine_field.mines

def game_load(board):
    cursor.move_cursor()
    board.render_board = RenderBoardCLI()
    render = board.render_board
    render.draw_board()
    render.draw_remaining_mines()
    prompt_row = board.depth * 2 + 6
    first_open_tile(board)

    while True:

        if board.remaining_mines == 0:
            correct_mines = 0

            for tile in board.tiles:
                if tile.is_mine and tile.is_flagged:
                    correct_mines += 1

            if correct_mines == len(board.mine_field.mines):
                return GameResult.WIN

        print_default_board_option(prompt_row)
        raw = input("Select Option: ").strip()
        pos = parse_tile_input(raw)
        
        if raw == "Q":
            return GameResult.QUIT
        
        elif pos is not None:
            while True:

                print_tile_options(prompt_row)
                action = input("Select Option: ").strip()

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
                    if reveal == RevealType.ISFLAGGED:
                        cursor.input_invalid(pos, prompt_row, "flag")
                    if reveal == RevealType.ISMINE:
                        return GameResult.LOSS
                    else:
                        render.update_tile_symbol(tile)
                        render.draw_tile(tile)

                        flood_reveal(tile, render)
                        break
            
        else:
            cursor.input_invalid(raw, prompt_row, "state")

def main():
    handle_first_load()
    
    saved_mines = None

    while True:
        menu_action = menu_load()

        if menu_action == MenuAction.START:

            while True:
                game_result, saved_mines = start_game(saved_mines)

                if game_result == GameResult.QUIT:
                    break

                else:
                    if game_result == GameResult.WON:
                        post_game_action = game_won()
                    elif game_result == GameResult.LOSS:
                        post_game_action = game_over()
                    else:
                        post_game_action = PostGameAction.MENU
                    

                    if post_game_action == PostGameAction.RESTART:
                        continue
                    elif post_game_action == PostGameAction.MENU:
                        saved_mines = None
                        break
                    elif post_game_action == PostGameAction.QUIT:
                        return quit_game()

        elif menu_action == MenuAction.QUIT:
            break

    quit_game()


if __name__ == "__main__":
    main()