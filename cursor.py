def reset_line():
    ANSI_reset = "\033[K"
    
    print_wo_newline(ANSI_reset)

def input_invalid(arg, usage=None, width=None, depth=None):
    
    if usage == None:
        print_w_flush(f'Invalid Selection "{arg}". Please try again.')
    elif usage == "locked":
        print_w_flush(f'Invalid Selection "{arg}. Currently Locked. Check back next update.')
    elif usage == "state":
        print_w_flush(f'Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2')
    elif usage == "coords":
        print_w_flush(f'Invalid Selection "{arg}". Tile Indices out of range "1-{depth}"')
    elif usage == "range":
        print_w_flush(f'Invalid Range "{arg}". Must be integer between 2 and {width - 2}')
    elif usage == "reveal":
        print_w_flush(f'Invalid Action. Tile at {arg} is already revealed!')
    elif usage == "flag":
        print_w_flush(f'Invalid Action. Tile at {arg} is Flagged. To reveal, first unflag Tile.')

def input_valid(arg):
    
    print_w_flush(f'Input {arg} accepted!')

def print_w_flush(string):
    print(string, flush=True)

def print_wo_newline(string):
    print(string, end="", flush=True)

def print_default_board_option(row):

    print_w_flush('Input "row,col" to select Tile, or "Q" for Quit')

def print_tile_options(row):

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
    
    if coords[0].isdigit() == False or coords[1].isdigit() == False:
        return None

    row = int(coords[0])
    col = int(coords[1])
    return (row, col)
  