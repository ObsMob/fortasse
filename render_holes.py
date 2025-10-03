from config import SymbolIcon

def holes_symbol_update(r, c, icon, board):
    board.board_render.cli_grid[r][c] = icon

def update_tile_borders(tile, board):
    cardinal_offsets = {
        "left": {
            "offset": (0, -1),
            "symbol": SymbolIcon.EMPTY_S.value,
            },
        "up": {
            "offset": (-1, 0),
            "symbol": SymbolIcon.EMPTY_D.value,
            },
        "right": {
            "offset": (0, +1),
            "symbol": SymbolIcon.EMPTY_S.value,
            },
        "down": {
            "offset": (+1, 0),
            "symbol": SymbolIcon.EMPTY_D.value,
            },
    }
    r, c = tile.state_coords

    for key in cardinal_offsets:
        dr, dc = cardinal_offsets[key]["offset"]
        icon = cardinal_offsets[key]["symbol"]
        coords = (r + dr, c + dc)
        neighbor = board.get_tile_from_coords(coords)

        if neighbor == None or neighbor.is_hole:
            cli_r, cli_c = board.board_render.state_to_cli_index(tile.state_coords)
            cli_r += dr
            cli_c += dc
            holes_symbol_update(cli_r, cli_c, icon, board)

def update_outline_intersections(board):
    grid = board.board_render.cli_grid
    diagonal_offsets = {
        "up_left": (-1, -1),
        "up_right": (-1, +1),
        "down_right": (+1, +1),
        "down_left": (+1, -1),
    }
    diagonal_icons = {
        "1111": SymbolIcon.EMPTY_S.value,
        "1110": SymbolIcon.TOPRIGHT.value,
        "1101": SymbolIcon.TOPLEFT.value,
        "1011": SymbolIcon.BOTLEFT.value,
        "0111": SymbolIcon.BOTRIGHT.value,
        "0011": SymbolIcon.BOTTEE.value,
        "0110": SymbolIcon.RIGHTTEE.value,
        "1100": SymbolIcon.TOPTEE.value,
        "1001": SymbolIcon.LEFTTEE.value,
    }
    
    for r in range(len(grid)):
        for c in range(len(grid[r])):

            if r % 2 == 1 and c % 2 == 1:
                bitwise = ""

                for key in diagonal_offsets:
                    dr, dc = diagonal_offsets[key]
                    state_coords = ((r + dr) // 2, (c + dc) // 2)
                    tile = board.get_tile_from_coords(state_coords)

                    if tile == None or tile.is_hole:
                        bitwise = bitwise + "1"
                    else:
                        bitwise = bitwise + "0"
                
                if bitwise in diagonal_icons:
                    holes_symbol_update(r, c, diagonal_icons[bitwise], board)

def cli_holes_render(board):

    for tile in board.tiles.values():
        if tile.is_hole:
            update_tile_borders(tile, board)
    
    update_outline_intersections(board)
