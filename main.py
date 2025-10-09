import sys
from blessed import Terminal

import cursor
from game_settings import load_settings, update_setting, save_settings
from render_menu import RenderMenuCLI
from game import game_init, game_won, game_over
from config import (
    PostGameAction,
    GameResult,
    MenuAction,
    Menu,
    Resolutions,
    TileShape,
    TextColor,
)

settings = load_settings()

def handle_first_load(settings):
    if settings["FIRST_LOAD"]:
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

def menu_start(settings, term):
    menu = RenderMenuCLI(settings)
    valid = False
    invalid = False
    invalid_range = False
    invalid_locked = False
    user_input = ""
    
    while True:
        cursor.print_w_flush(term.clear + term.home)
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
                    cursor.reset_line()
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "S":
                        return MenuAction.START
                    elif user_input == "G":
                        menu.options_menu = Menu.GAMESETT
                    elif user_input == "U":
                        menu.options_menu = Menu.UISETT
                    elif user_input == "Q":
                        return MenuAction.QUIT
                    else:
                        invalid = True
                    break
                continue

            case Menu.GAMESETT:
                while True:
                    cursor.reset_line()
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.MAIN
                    elif user_input == "S":
                        menu.options_menu = Menu.DEPTH
                    elif user_input == "T":
                        menu.options_menu = Menu.TILE
                    elif user_input == "C":
                        if settings["CORNERS"]:
                            update_setting("CORNERS", False, settings)
                        else:
                            update_setting("CORNERS", True, settings) 
                    elif user_input == "H":
                        if settings["HOLES"]:
                            update_setting("HOLES", False, settings)
                        else:
                            update_setting("HOLES", True, settings)  
                    elif user_input == "U":
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

            case Menu.DEPTH:
                while True:
                    cursor.reset_line()
                    user_input = input("Select Option: ").strip().upper()
                    
                    if user_input == "B":
                        menu.options_menu = Menu.GAMESETT
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
                    cursor.reset_line()                
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.GAMESETT
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

            case Menu.UISETT:
                while True:
                    cursor.reset_line()              
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.MAIN
                    elif user_input == "R":
                        menu.options_menu = Menu.RES
                    elif user_input == "W":
                        if settings["WASD"]:
                            update_setting("WASD", False, settings)
                        else:
                            update_setting("WASD", True, settings)
                    elif user_input == "F":
                        if settings["AUTO_BACK"]:
                            update_setting("AUTO_BACK", False, settings)
                        else:
                            update_setting("AUTO_BACK", True, settings)
                    else:
                        invalid = True
                        break
                    menu.populate_options_sections()
                    valid = True
                    break
                continue

            case Menu.RES:
                while True:
                    cursor.reset_line()                 
                    user_input = input("Select Option: ").strip().upper()

                    if user_input == "B":
                        menu.options_menu = Menu.UISETT
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
                    valid = True
                    break
                continue

def main(settings):
    
    handle_first_load(settings)
    
    term = Terminal()
    with term.fullscreen():

        while True:
            restart = False
            board = None
            menu_action = menu_start(settings, term)
            
            if menu_action == MenuAction.START:

                while True:
                    game_result, board = game_init(settings, term, board, restart)

                    if game_result == GameResult.QUIT:
                        break
                    elif game_result == GameResult.WIN:
                        post_game_action = game_won(settings, board)
                    elif game_result == GameResult.LOSS:
                        post_game_action = game_over(board)

                    if post_game_action == PostGameAction.RESTART:
                        restart = True
                        continue
                    elif post_game_action == PostGameAction.MENU:
                        break
                    elif post_game_action == PostGameAction.QUIT:
                        save_settings(settings)
                        return

            elif menu_action == MenuAction.QUIT:
                break

        save_settings(settings)
    quit_game()


if __name__ == "__main__":
    main(settings)