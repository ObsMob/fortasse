def move_cursor(row=1, column=1):
    move_cursor = f'\033[{row};{column}H'
    
    print_wo_newline(move_cursor)
    
def reset_line():
    ANSI_reset = "\033[K"
    
    print_wo_newline(ANSI_reset)

def cursor_to_prompt(row):
    
    move_cursor(row, 15) # 15 is default column position = len("Select option: ")

def cursor_to_sys_msg(row):
    
    move_cursor(row - 1)
    reset_line()

def input_invalid(arg, row, usage=None, width=4):
    
    cursor_to_sys_msg(row)

    if usage == None:
        print_wo_newline(f'Invalid Selection "{arg}". Please try again.')
    elif usage == "locked":
        print_wo_newline(f'Invalid Selection "{arg}. Currently Locked. Check back next update.')
    elif usage == "state":
        print_wo_newline(f'Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2')
    elif usage == "range":
        print_wo_newline(f'Invalid Range "{arg}". Must be integer between 2 and {width - 2}')
    elif usage == "reveal":
        print_wo_newline(f'Invalid Action. Tile at {arg} is already revealed!')
    elif usage == "flag":
        print_wo_newline(f'Invalid Action. Tile at {arg} is Flagged. To reveal, first unflag Tile.')
    
    cursor_to_prompt(row)

def input_valid(arg, row):
    
    cursor_to_sys_msg(row) 
    print_wo_newline(f'Input {arg} accepted!')
    cursor_to_prompt(row)

def print_w_flush(string):
    print(string, flush=True)

def print_wo_newline(string):
    print(string, end="", flush=True)

def print_default_board_option(row):
    cursor_to_sys_msg(row)
    print_w_flush('Input "row,col" to select Tile, or "Q" for Quit')
    cursor_to_prompt(row)

def print_tile_options(row):
    cursor_to_sys_msg(row)
    print_wo_newline('Input "F" for Flag/Unflag, "R" for Reveal, or "B" for Back')
    cursor_to_prompt(row)

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
    
    if coords[0].isdigit() == False or coords[1].isdigit() == False:
        return None

    row = int(coords[0])
    col = int(coords[1])
    return (row, col)
  