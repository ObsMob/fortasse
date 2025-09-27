import itertools

def build_constraints(revealed_working):
    constraints = []

    for tile in revealed_working:
        unrevealed = set(n for n in tile.neighbors if not n.is_revealed and not n.is_flagged)
        mines_left= tile.adjacent_mines - tile.adjacent_flags
        
        if unrevealed:
            constraints.append((unrevealed, mines_left))
            
    return constraints

def build_components(constraints):
    visited = set()
    possible_tiles = set()
    components = []

    for tile_set, _ in constraints:
        possible_tiles.update(tile_set)

    for tile in possible_tiles:
        if tile in visited:
            continue

        new_component = set()
        stack = [tile]
        while stack:

            t = stack.pop()
            if t in visited:
                continue

            visited.add(t)
            new_component.add(t)

            for n in t.neighbors:
                if n in possible_tiles and n not in visited:
                    
                    stack.append(n)

        components.append(new_component)

    return components  

def constraint_to_index(constraints, component):
    tile_to_index = {tile: idx for idx, tile in enumerate(component)}
    indexed_constraint = []

    for tiles, mine_count in constraints:

        # get 'index' from built dictionary, for each tile in a single constraint, so long as it's part of the component
        indices = tuple(tile_to_index[tile] for tile in tiles if tile in component)

        if mine_count < 0 or mine_count > len(indices):
            return [], True
        else: 
            indexed_constraint.append((indices, mine_count))

    return indexed_constraint, False

def bitwise_index_check(indexed_constraint, component):
    # creates a list of 'bit' vectors(?), eg {0,0}, {0,1}, {1,0}, {1,1} to check against index based constraint.
    # if all iterations of checking the bit vectors against each index in the component return the same value,
    # that value = forced tile attribute at index of constraint.
    passed_assignment = []

    for possible_deduction in itertools.product((0,1), repeat=len(component)):
        ok = True

        for indices, mine_count in indexed_constraint:
            if sum(possible_deduction[i] for i in indices) != mine_count:
                ok = False
                break
        if ok:
            passed_assignment.append(possible_deduction)

    if not passed_assignment:
        return [], True
    else:
        return passed_assignment, False

def enumerate_and_check(passed_assignment, component):
    to_reveal = set()
    to_flag = set()

    for i, tile in enumerate(component):
        possibilities = set(assignment[i] for assignment in passed_assignment)
        
        if len(possibilities) == 1:
            bit = possibilities.pop()

            if bit == 0:
                to_reveal.add(tile)
            else:
                to_flag.add(tile)

    return to_reveal, to_flag

def solve_component(constraints, component):
    
    indexed_constraint, error = constraint_to_index(constraints, component)
    if error:
        # log error - mine_count from constraints invalid
        return set(), set()

    passed_assignment, error = bitwise_index_check(indexed_constraint, component)
    if error:
        # log error - no passed_assignment. check mines list & component state_coords
        return set(), set()

    to_reveal, to_flag = enumerate_and_check(passed_assignment, component)
    return to_reveal, to_flag
    
def global_enumerate_and_deduce(revealed_working):
    constraints = build_constraints(revealed_working)
    components = build_components(constraints)

    to_reveal = set()
    to_flag = set()

    for component in components:
        r, f = solve_component(constraints, component)

        to_reveal.update(r)
        to_flag.update(f)

    conflicts = to_reveal & to_flag
    if conflicts:
        # log conflicts
        to_reveal -= conflicts
        to_flag -= conflicts

    return to_reveal, to_flag
