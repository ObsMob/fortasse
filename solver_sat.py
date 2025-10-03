from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def build_constraints(revealed_working):
    constraints = []

    for tile in revealed_working:
        unrevealed = set(n for n in tile.neighbors if not n.is_revealed and not n.is_flagged)
        mines_left= tile.adjacent_mines - tile.adjacent_flags
        
        if unrevealed:
            constraints.append((unrevealed, mines_left))
            
    return constraints

def build_components(constraints):
    
    possible_tiles = set()
    for tile_set, _ in constraints:
        possible_tiles.update(tile_set)

    # must build component map from constraints, instead of simply mapping neighbors
    adjacency_map  = {tile: set() for tile in possible_tiles} 
    for tile_set, _ in constraints:
        tile_list = list(tile_set)

        for i in range(len(tile_list)):
            for j in range(i+1, (len(tile_list))):
                a = tile_list[i]
                b = tile_list[j]
                adjacency_map[a].add(b)
                adjacency_map[b].add(a)

    visited = set()
    components = []
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

            for neighbor in adjacency_map[t]:
                if neighbor not in visited:
                    
                    stack.append(neighbor)

        components.append(new_component)

    return components  

def build_cnf(comp_constraints, component):
    tiles = list(component)
    tile_to_variable= {tile: i+1 for i, tile in enumerate(tiles)}
    cnf = CNF()

    for tile_set, mine_count in comp_constraints:
        sat_variables = [tile_to_variable[t] for t in tile_set]

        if not sat_variables:
            continue

        if mine_count < 0 or mine_count > len(sat_variables):
            continue

        atleast = CardEnc.atleast(sat_variables, bound=mine_count, encoding=EncType.seqcounter)    
        atmost = CardEnc.atmost(sat_variables, bound=mine_count, encoding=EncType.seqcounter)
        cnf.extend(atleast.clauses)
        cnf.extend(atmost.clauses)

    if not cnf.clauses:
        return cnf, tile_to_variable, False
    else:
        return cnf, tile_to_variable, True

def solve_component_sat(cnf, tile_to_variable):
    to_reveal = set()
    to_flag = set()

    with Solver(bootstrap_with=cnf) as solver:
        
        sat = solver.solve()
        if not sat:
            return set(), set()

        model = solver.get_model() or []
        model_map = {abs(var): (var > 0) for var in model}
        
        for tile, var in tile_to_variable.items():
            is_mine = model_map.get(var, False)

            if is_mine:
                counter = solver.solve(assumptions=[-var])
                if not counter:
                    to_flag.add(tile)
            else:
                counter = solver.solve(assumptions=[var])
                if not counter:
                    to_reveal.add(tile)

    return to_reveal, to_flag

def global_sat_deduction(revealed_working):
    
    constraints = build_constraints(revealed_working)
    if not constraints:
        return set(), set()

    components = build_components(constraints)

    to_reveal = set()
    to_flag = set()

    for component in components:
        comp_constraints = [(tiles, k) for (tiles, k) in constraints if set(tiles).issubset(component)]
        
        cnf, tile_to_variable, ok = build_cnf(comp_constraints, component)
        if not ok:
            # log cnf, tile map, component and constraints
            continue

        r, f = solve_component_sat(cnf, tile_to_variable)

        to_reveal.update(r)
        to_flag.update(f)

    conflicts = to_reveal & to_flag
    if conflicts:
        # log conflicts
        to_reveal -= conflicts
        to_flag -= conflicts

    return to_reveal, to_flag
