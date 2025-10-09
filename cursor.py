from config import TextColor


def reset_line():
    ANSI_reset = "\033[K"
    
    print_wo_newline(ANSI_reset)

def input_invalid(invalid, arg, usage=None, width=None, depth=None):
    
    if invalid:
        if arg == "":
            arg = "_"
        if usage == None:
            print_w_flush(f'{TextColor.RED.value}Invalid Selection "{arg}". Please try again.{TextColor.RESET.value}')
        elif usage == "locked":
            print_w_flush(f'{TextColor.RED.value}Invalid Selection "{arg}". Currently Locked. Check back next update.{TextColor.RESET.value}')
        elif usage == "state":
            print_w_flush(f'{TextColor.RED.value}Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2{TextColor.RESET.value}')
        elif usage == "coords":
            print_w_flush(f'{TextColor.RED.value}Invalid Tile Indices "{arg}". Tile Indices out of range "1-{depth}"{TextColor.RESET.value}')
        elif usage == "range":
            print_w_flush(f'{TextColor.RED.value}Invalid Range "{arg}". Must be integer between 2 and {(width - 2) // 3}{TextColor.RESET.value}')
        elif usage == "reveal":
            print_w_flush(f'{TextColor.RED.value}Invalid Action. Tile at {arg} is already Revealed!{TextColor.RESET.value}')
        elif usage == "flag":
            print_w_flush(f'{TextColor.RED.value}Invalid Action. Tile at {arg} is Flagged. To Reveal, first Unflag Tile.{TextColor.RESET.value}')      
    else:
        print_w_flush("")

def input_valid(valid, arg, usage=None):

    if valid:
        if usage == None:
            print_w_flush(f'{TextColor.GREEN.value}Input "{arg}" accepted!{TextColor.RESET.value}')
        if usage == "flag":
            print_w_flush(f'{TextColor.GREEN.value}Tile at {arg} has been Flagged.{TextColor.RESET.value}')            
        if usage == "unflag":
            print_w_flush(f'{TextColor.GREEN.value}Tile at {arg} has been Unflagged.{TextColor.RESET.value}')            
        if usage == "reveal":
            print_w_flush(f'{TextColor.GREEN.value}Tile at {arg} has been Revealed.{TextColor.RESET.value}')
        if usage == "move":
            print_w_flush(f'{TextColor.GREEN.value}Tile at {arg} has been Chosen.{TextColor.RESET.value}')                         
    else:
        print_w_flush("")

def print_w_flush(string):
    print(f'\033[K{string}', flush=True)

def print_wo_newline(string):
    print(f'\033[K{string}', end="", flush=True)

def print_default_board_option(settings):

    if settings["WASD"]:
        print_w_flush('"WASD/Arrow" to navigate, "ENTER" for select, or "ESC" for Quit')
    else:
        print_w_flush('Input "row,col" to select Tile, or "Q" for Quit')

def print_tile_options():

    print_w_flush('Input "F" for Flag/Unflag, "R" for Reveal, or "B" for Back')

def parse_tile_input(raw_string):
    user_input = raw_string
    coords = []

    for sep in [",", "<", ".", ">", ";", ":", "'", '"', "-", "_"]:
        user_input = user_input.replace(sep, " ")

    split_coords = user_input.split()

    for coord in split_coords:
        coord = coord.strip()
        if coord != "":
            coords.append(coord)

    if len(coords) != 2:
        return None
    
    if not coords[0].isdigit() or not coords[1].isdigit():
        return None

    row = int(coords[0])
    col = int(coords[1])
    return (row, col)

def deduction_load_wait(ellipsis):
    if ellipsis == "....":
        ellipsis = "."
    else:
        ellipsis += "."

    print_wo_newline("\r")
    print_wo_newline(f'Checking for deducible Board{ellipsis}')
    return ellipsis
