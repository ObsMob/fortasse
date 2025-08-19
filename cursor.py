def move_cursor(row=1, column=1):
    move_cursor = f'\033[{row};{column}H'
    
    print(move_cursor, end="", flush=True)
    
def reset_line():
    ANSI_reset = "\033[K"
    
    print(ANSI_reset, end="", flush=True)

def cursor_to_prompt(row):
    
    ansi_move_cursor(row, 15) # 15 is default column position = len("Select option: ")

def cursor_to_sys_msg(row):
    
    ansi_move_cursor(row - 1)
    reset_line()

def input_invalid(arg, row, width=4, usage=None):
    
    cursor_to_sys_msg(row)

    if usage == None:
        print(f'Invalid Selection "{arg}". Please try again.', end="", flush=True)
    elif usage == "locked":
        print(f'Invalid Selection "{arg}. Currently Locked. Check back next update.', end="", flush=True)
    elif usage == "state_index"
        print(f'Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2', end="", flush=True)
    elif usage == "range":
        print(f'Invalid Range "{arg}". Must be between 2 and {width - 2}', end="", flush=True)
    
    cursor_to_prompt(row)

def input_valid(arg, row):
    
    cursor_to_sys_msg(row) 
    print(f'Input {arg} accepted!', end="", flush=True)
    cursor_to_prompt(row)

def print_w_newline(string):
    print(string, flush=True)

def print_wo_newline(string):
    print(string, end="", flush=True)