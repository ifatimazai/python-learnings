# sudoku_csp.py — Sudoku solver + generator using CSP (AC-3, MRV, LCV)

import random, sys, copy
from typing import Dict, List, Tuple, Optional, Set

Digits = '123456789'
Rows = 'ABCDEFGHI'
Cells = [r + c for r in Rows for c in Digits]

def cross(A, B):  # Cartesian product
    return [a + b for a in A for b in B]

# Units and peers
row_units = [cross(r, Digits) for r in Rows]
col_units = [cross(Rows, c) for c in Digits]
box_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + col_units + box_units
units = {s: [u for u in unitlist if s in u] for s in Cells}
peers = {s: set(sum(units[s], [])) - {s} for s in Cells}

def parse_grid(grid_str):  # Parse 81-char grid
    grid_str = ''.join(ch for ch in grid_str if ch in Digits + '0.')
    if len(grid_str) != 81:
        raise ValueError("Grid must have 81 chars")
    return {Cells[i]: (grid_str[i] if grid_str[i] in Digits else '.') for i in range(81)}

def display(values):  # Pretty print
    width = 1 + max(len(values[s]) for s in Cells)
    line = '+'.join(['-'*(width*3)]*3)
    for r in Rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in Digits))
        if r in 'CF': print(line)
    print()

def grid_values_to_domains(grid):  # Convert to domains
    return {s: Digits[:] if grid[s] == '.' else grid[s] for s in Cells}

# AC-3 constraint propagation
def ac3(domains):
    queue = [(xi, xj) for xi in Cells for xj in peers[xi]]
    while queue:
        xi, xj = queue.pop(0)
        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False
            for xk in peers[xi] - {xj}:
                queue.append((xk, xi))
    return True
def revise(domains, xi, xj):  # Remove unsupported values
    revised = False
    for d in domains[xi]:
        if all(d == dj for dj in domains[xj]):
            domains[xi] = domains[xi].replace(d, '')
            revised = True
    return revised

# Assignment + forward checking
def assign(domains, var, val):
    new = copy.deepcopy(domains)
    new[var] = val
    for p in peers[var]:
        if val in new[p]:
            new[p] = new[p].replace(val, '')
            if len(new[p]) == 0:
                return None
    if not ac3(new):
        return None
    return new

# MRV heuristic
def select_unassigned_variable(domains):
    unassigned = [v for v in Cells if len(domains[v]) > 1]
    return min(unassigned, key=lambda v: len(domains[v])) if unassigned else next(iter(Cells))

# LCV heuristic
def order_domain_values(domains, var):
    values = list(domains[var])
    def conflicts(val): return sum(1 for p in peers[var] if val in domains[p])
    return sorted(values, key=conflicts)

# Backtracking search
def backtracking_search(domains):
    if all(len(domains[s]) == 1 for s in Cells):
        return domains
    var = select_unassigned_variable(domains)
    for val in order_domain_values(domains, var):
        new_domains = assign(domains, var, val)
        if new_domains is not None:
            result = backtracking_search(new_domains)
            if result is not None:
                return result
    return None

def solve(grid):  # Solver wrapper
    grid = parse_grid(grid) if isinstance(grid, str) else grid
    domains = grid_values_to_domains(grid)
    if not ac3(domains): return None
    return backtracking_search(domains)

# Count solutions (used for puzzle generation)
def count_solutions(domains, limit=2):
    count, stack = 0, [domains]
    while stack:
        cur = stack.pop()
        if all(len(cur[s]) == 1 for s in Cells):
            count += 1
            if count >= limit: return count
            continue
        var = select_unassigned_variable(cur)
        for val in order_domain_values(cur, var):
            new = assign(cur, var, val)
            if new is not None: stack.append(new)
    return count

def random_solution():  # Full random grid
    domains = {s: Digits[:] for s in Cells}
    def order_vals_random(dom, var):
        vals = list(dom[var]); random.shuffle(vals); return vals
    def solve_random(dom):
        if all(len(dom[s]) == 1 for s in Cells): return dom
        var = select_unassigned_variable(dom)
        for v in order_vals_random(dom, var):
            new = assign(dom, var, v)
            if new is not None:
                sol = solve_random(new)
                if sol is not None: return sol
        return None
    sol = solve_random(domains)
    if sol is None: raise RuntimeError("Failed to generate solution")
    return sol

def domains_to_grid_string(dom):  # Convert domains -> 81-char string
    return ''.join(dom[s] if len(dom[s]) == 1 else '.' for s in Cells)

def generate_puzzle(clues=30, max_tries=1000):
    if not (17 <= clues <= 81):
        raise ValueError("Clues must be 17–81")
    sol = random_solution()
    full = domains_to_grid_string(sol)
    puzzle = list(full)
    positions = Cells[:]
    random.shuffle(positions)
    removals = 81 - clues
    tries = 0
    for pos in positions:
        if removals <= 0: break
        if tries > max_tries: break
        tries += 1
        i = Cells.index(pos)
        backup = puzzle[i]
        puzzle[i] = '.'
        dom = grid_values_to_domains({Cells[idx]: (puzzle[idx] if puzzle[idx] in Digits else '.') for idx in range(81)})
        if not ac3(dom) or count_solutions(dom, limit=2) != 1:
            puzzle[i] = backup
        else:
            removals -= 1
    return ''.join(puzzle), full

EXAMPLE = (
    '53..7....'
    '6..195...'
    '.98....6.'
    '8...6...3'
    '4..8.3..1'
    '7...2...6'
    '.6....28.'
    '...419..5'
    '....8..79'
)
def print_grid_from_string(g): display(grid_values_to_domains(parse_grid(g)))
if __name__ == '__main__':
    print("Example puzzle:"); print_grid_from_string(EXAMPLE)
    print("Solving..."); sol = solve(EXAMPLE)
    display(sol if sol else {"ERR":"No solution"})
    print("Generating puzzle...")
    p, s = generate_puzzle(clues=28, max_tries=5000)
    print("Puzzle:"); print_grid_from_string(p)
    print("Solution:"); print_grid_from_string(s)
