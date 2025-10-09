from config import KeyPress


def get_keypress(term):

    with term.cbreak():
        key = term.inkey(timeout=None)

        if key.is_sequence:

            if key.name == "KEY_UP":
                return KeyPress.UP
            elif key.name == "KEY_DOWN":
                return KeyPress.DOWN
            elif key.name == "KEY_RIGHT":
                return KeyPress.RIGHT
            elif key.name == "KEY_LEFT":
                return KeyPress.LEFT
            elif key.name == "KEY_ENTER":
                return KeyPress.SELECT
            elif key.name == "KEY_ESCAPE":
                return KeyPress.QUIT
        else:

            if key.upper() == "W":
                return KeyPress.UP
            elif key.upper() == "S":
                return KeyPress.DOWN
            elif key.upper() == "D":
                return KeyPress.RIGHT
            elif key.upper() == "A":
                return KeyPress.LEFT
        return None

def wasd_walk(board, delta):
    base_r, base_c = board.selected.state_coords
    dr, dc = delta.value

    # shifts row/column counter clockwise
    shift_r, shift_c = -dc, dr

    for i in range(board.depth):
        # shift per iteration
        cur_r, cur_c = base_r + shift_r * i, base_c + shift_c * i
        cur_r, cur_c = wrap_check(cur_r, cur_c, board)

        for _ in range(board.depth-1):
            cur_r, cur_c = cur_r + dr, cur_c + dc
            cur_r, cur_c = wrap_check(cur_r, cur_c, board)
            
            tile = board.get_tile_from_coords((cur_r, cur_c))

            if tile is not None and not tile.is_hole:
                return tile

def wrap_check(r, c, board):
    # 1 based index wrap modulus. 0 based index simply: r, c = r%depth, c%depth
    r = (((r - 1) % board.depth) + 1)
    c = (((c - 1) % board.depth) + 1)
    return r, c
