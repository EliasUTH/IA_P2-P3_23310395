import random

def min_conflicts_search(variables, domains, constraints, max_steps=1000):
    """
    Búsqueda local con heurística de mínimos conflictos (min-conflicts).

    Parámetros:
    - variables: lista de variables
    - domains: diccionario {variable: lista de valores}
    - constraints: lista de tuplas (var1, var2, función_restricción)
    - max_steps: máximo número de pasos

    Retorna: asignación completa o None si no converge.
    """
    def count_conflicts(var, value, assignment):
        """Cuenta conflictos para una variable con un valor dado."""
        conflicts = 0
        for (var1, var2, constraint) in constraints:
            if var1 == var and var2 in assignment:
                if not constraint(value, assignment[var2]):
                    conflicts += 1
            if var2 == var and var1 in assignment:
                if not constraint(assignment[var1], value):
                    conflicts += 1
        return conflicts

    def total_conflicts(assignment):
        """Cuenta total de conflictos en la asignación."""
        conflicts = 0
        for var in variables:
            conflicts += count_conflicts(var, assignment[var], assignment)
        return conflicts // 2  # Cada conflicto se cuenta dos veces

    # Asignación inicial aleatoria
    assignment = {var: random.choice(domains[var]) for var in variables}

    for _ in range(max_steps):
        if total_conflicts(assignment) == 0:
            return assignment  # Solución encontrada

        # Encontrar variable con más conflictos
        conflicted_vars = [var for var in variables if count_conflicts(var, assignment[var], assignment) > 0]
        if not conflicted_vars:
            return assignment  # No hay conflictos

        var = random.choice(conflicted_vars)

        # Encontrar valor con menos conflictos para esa variable
        best_value = assignment[var]
        min_conflicts = count_conflicts(var, best_value, assignment)
        for value in domains[var]:
            if value != assignment[var]:
                conflicts = count_conflicts(var, value, assignment)
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_value = value

        assignment[var] = best_value

    return None  # No convergió

# Ejemplo de uso: Problema de las 4-Reinas
print("=== Búsqueda Local Mínimos Conflictos (4-Reinas) ===")
n = 4
variables = [f'Q{i}' for i in range(n)]
domains = {v: list(range(n)) for v in variables}  # Columnas 0-3

def queens_constraint(col1, col2, row1, row2):
    return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)

constraints = []
for i in range(n):
    for j in range(i+1, n):
        var1, var2 = f'Q{i}', f'Q{j}'
        constraints.append((var1, var2, lambda x, y, i=i, j=j: queens_constraint(x, y, i, j)))

random.seed(42)
solution = min_conflicts_search(variables, domains, constraints, max_steps=100)

if solution:
    print("Solución encontrada:")
    for queen in sorted(solution.keys()):
        print(f"  {queen}: columna {solution[queen]}")
else:
    print("No se encontró solución en el límite de pasos.")