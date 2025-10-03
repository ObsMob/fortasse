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

    # create the bit vector list
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

def solve_component_sat(constraints, component):
    
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
    