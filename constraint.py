import itertools







def _solve_component_exact(constraints, comp_vars, max_vars=None):
    """
    Solve one component by enumerating all assignments to its variables.
    Returns (to_reveal_set, to_flag_set, inconsistent_flag, skipped_flag).
    - skipped_flag True if we skipped due to max_vars limit.
    """
    vars_list = list(comp_vars)
    v = len(vars_list)
    if max_vars is not None and v > max_vars:
        return set(), set(), False, True  # skip this component

    var_index = {tile: idx for idx, tile in enumerate(vars_list)}

    # Pick constraints relevant to this component and build index-based equations
    eqs = []
    for tileset, cnt in constraints:
        if tileset & comp_vars:
            indices = tuple(var_index[t] for t in tileset if t in var_index)
            # Sanity check: cnt must be in [0, len(indices)]
            if cnt < 0 or cnt > len(indices):
                return set(), set(), True, False  # inconsistent component
            eqs.append((indices, cnt))

    # Enumerate all assignments for this component
    satisfying = []
    for bits in itertools.product((0,1), repeat=v):
        ok = True
        for indices, cnt in eqs:
            if sum(bits[i] for i in indices) != cnt:
                ok = False
                break
        if ok:
            satisfying.append(bits)

    if not satisfying:
        return set(), set(), True, False  # inconsistent component

    # Find forced variables (same value in every satisfying assignment)
    to_reveal = set()
    to_flag = set()
    for idx, tile in enumerate(vars_list):
        vals = {assign[idx] for assign in satisfying}
        if len(vals) == 1:
            val = next(iter(vals))
            if val == 1:
                to_flag.add(tile)
            else:
                to_reveal.add(tile)

    return to_reveal, to_flag, False, False