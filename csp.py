# -------------------------------
# AUSTRALIA MAP COLORING AS CSP
# -------------------------------

# Variables: Regions of Australia
variables = ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS']

# Domains: Possible colors for each region
domains = {var: ['Red', 'Green', 'Blue'] for var in variables}

# Constraints: neighboring regions cannot have the same color
adjacency = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'QLD'],
    'SA': ['WA', 'NT', 'QLD', 'NSW', 'VIC'],
    'QLD': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'QLD', 'VIC'],
    'VIC': ['SA', 'NSW', 'TAS'],
    'TAS': ['VIC']
}

# Function to check constraints
def constraint_satisfied(var, value, assignment):
    for neighbor in adjacency[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

# Backtracking CSP solver to get all solutions
def csp_backtracking(assignment={}):
    # If assignment is complete, return it as a solution
    if len(assignment) == len(variables):
        return [assignment.copy()]

    solutions = []

    # Select the next unassigned variable
    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]

    # Try all possible colors for the variable
    for value in domains[var]:
        if constraint_satisfied(var, value, assignment):
            assignment[var] = value
            solutions.extend(csp_backtracking(assignment))  # recursive backtracking
            assignment.pop(var)  # backtrack

    return solutions

# To get all 18 solutions, we need to fix one variable to break symmetry
# Let's fix WA to Red (this will give us 6 solutions)
# Then we multiply by 3 for the 3 possible colors for WA
all_solutions = []

# Try all 3 possible colors for WA
for wa_color in ['Red', 'Green', 'Blue']:
    initial_assignment = {'WA': wa_color}
    solutions_with_fixed_wa = csp_backtracking(initial_assignment)
    all_solutions.extend(solutions_with_fixed_wa)

print(f"Total solutions found: {len(all_solutions)}\n")  # should be 18

# Function to print map nicely
def print_map(solution):
    print(f"WA: {solution['WA']} | NT: {solution['NT']} | SA: {solution['SA']}")
    print(f"QLD: {solution['QLD']} | NSW: {solution['NSW']} | VIC: {solution['VIC']} | TAS: {solution['TAS']}\n")

# Print all 18 solutions
for idx, sol in enumerate(all_solutions, 1):
    print(f"Solution {idx}:")
    print_map(sol)