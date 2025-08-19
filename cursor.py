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
    elif usage == "state_index"
        print_wo_newline(f'Invalid Selection "{arg}". Usage: "1,2" for Row 1, Column 2')
    elif usage == "range":
        print_wo_newline(f'Invalid Range "{arg}". Must be integer between 2 and {width - 2}')
    
    cursor_to_prompt(row)

def input_valid(arg, row):
    
    cursor_to_sys_msg(row) 
    print_wo_newline(f'Input {arg} accepted!')
    cursor_to_prompt(row)

def print_w_flush(string):
    print(string, flush=True)

def print_wo_newline(string):
    print(string, end="", flush=True)
