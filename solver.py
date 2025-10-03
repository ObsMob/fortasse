from solver_sat import global_sat_deduction


def zero_adjacent(tile):
    to_reveal = set()
    to_clear = set()

    if tile.adjacent_mines == 0:
        for neighbor in tile.neighbors:
            if not neighbor.is_revealed and not neighbor.is_flagged: 
            
                to_reveal.add(neighbor)

        to_clear.add(tile)

    return to_reveal, set(), to_clear

def adjacent_eq_flags(tile):
    to_reveal = set()
    to_clear = set()

    if tile.adjacent_mines == tile.adjacent_flags:
        for neighbor in tile.neighbors:
            if not neighbor.is_revealed and not neighbor.is_flagged:
                
                to_reveal.add(neighbor)
                
        to_clear.add(tile)

    return to_reveal, set(), to_clear

def adjacent_eq_unrevealed(tile):
    to_flag = set()
    to_clear = set()

    if tile.adjacent_mines - tile.adjacent_flags == sum(1 for n in tile.neighbors if not n.is_revealed and not n.is_flagged):
        for neighbor in tile.neighbors:
            if not neighbor.is_revealed and not neighbor.is_flagged:

                to_flag.add(neighbor)

        to_clear.add(tile)

    return set(), to_flag, to_clear

def subset_pair_compare(revealed_working):
    to_reveal = set()
    to_flag = set()

    for tile_a in revealed_working:
        unrevealed_a = set(n for n in tile_a.neighbors if not n.is_revealed and not n.is_flagged)
        mines_left_a = tile_a.adjacent_mines - tile_a.adjacent_flags
        
        for tile_b in revealed_working:
            if tile_a == tile_b:
                continue

            unrevealed_b = set(n for n in tile_b.neighbors if not n.is_revealed and not n.is_flagged)
            mines_left_b = tile_b.adjacent_mines - tile_b.adjacent_flags

            overlap = unrevealed_a & unrevealed_b
            non_overlap_a = unrevealed_a - overlap
            non_overlap_b = unrevealed_b - overlap

            if unrevealed_a <= unrevealed_b and mines_left_a <= mines_left_b:
                non_overlap_mines_b = mines_left_b - mines_left_a
                
                if non_overlap_mines_b == len(non_overlap_b):
                    to_flag.update(non_overlap_b)

                    left_over_mines = mines_left_b - len(non_overlap_b)
                    if left_over_mines == len(overlap):
                        to_flag.update(overlap) 

                    elif left_over_mines == 0:
                        to_reveal.update(overlap)   
                    
                    elif left_over_mines == mines_left_a:
                        to_reveal.update(non_overlap_a)
                
                elif non_overlap_mines_b == 0:
                    to_reveal.update(non_overlap_b)

                    if mines_left_b == len(overlap):
                        to_flag.update(overlap)

                        if len(overlap) == mines_left_a:
                            to_reveal.update(non_overlap_a)

    return to_reveal, to_flag

def solver_reveal_tiles(to_reveal, revealed_working):

    for tile in to_reveal:
        tile.reveal_tile()
        revealed_working.add(tile)

def solver_flag_tiles(to_flag, flagged):

    for tile in to_flag:
        tile.flag_tile()
        flagged.add(tile)

def solver_clear_tiles(to_clear, revealed_working, cleared):
    
    for tile in to_clear:
        revealed_working.remove(tile)
        cleared.add(tile)

def solver_win_state(cleared, flagged, board):
    must_clear = board.tile_quantity

    if board.holes:
        must_clear -= board.holes_quant

    return (
        len(cleared) + len(flagged) == must_clear and
        len(flagged) == board.mines_quant
    )

def solver(board):
    revealed_working = set()
    flagged = set()
    cleared = set()

    for tile in board.tiles.values():
        if tile.is_revealed:
            revealed_working.add(tile)

    while True:
        to_reveal = set()
        to_flag = set()
        to_clear = set()

        for tile in revealed_working:

            results = [
                zero_adjacent(tile),
                adjacent_eq_flags(tile),
                adjacent_eq_unrevealed(tile)
            ]
        
            for r, f, c in results:
                to_reveal.update(r)
                to_flag.update(f)
                to_clear.update(c)

        r, f = subset_pair_compare(revealed_working)
        to_reveal.update(r)
        to_flag.update(f)
        
        if to_reveal or to_clear or to_flag:

            solver_clear_tiles(to_clear, revealed_working, cleared)
            solver_flag_tiles(to_flag, flagged)
            solver_reveal_tiles(to_reveal, revealed_working)
            continue
        
        if solver_win_state(cleared, flagged, board):
            return True
        else:
            to_reveal, to_flag = global_sat_deduction(revealed_working)

            if to_reveal or to_flag:
                
                solver_flag_tiles(to_flag, flagged)
                solver_reveal_tiles(to_reveal, revealed_working)
                continue
            else:
                return False
