def backtracking_search(variables, domains, constraints):
    """
    Implementación básica de búsqueda por vuelta atrás (backtracking search).

    Parámetros:
    - variables: lista de variables
    - domains: diccionario {variable: lista de valores posibles}
    - constraints: lista de tuplas (var1, var2, función_restricción)

    Retorna:
    - Asignación completa si se encuentra solución
    - None si no hay solución
    """
    def is_consistent(var, value, assignment):
        for (var1, var2, constraint) in constraints:
            if var1 == var and var2 in assignment:
                if not constraint(value, assignment[var2]):
                    return False
            if var2 == var and var1 in assignment:
                if not constraint(assignment[var1], value):
                    return False
        return True

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment

        # Seleccionar siguiente variable sin asignar
        unassigned = [v for v in variables if v not in assignment]
        var = unassigned[0]

        for value in domains[var]:
            if is_consistent(var, value, assignment):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None

    return backtrack({})


# Ejemplo de uso: problema simple de coloreo de mapa
print("=== Ejemplo de Búsqueda por Vuelta Atrás ===")
variables = ['A', 'B', 'C', 'D']
domains = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
constraints = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

solution = backtracking_search(variables, domains, constraints)
if solution:
    print("Solución encontrada:")
    for var, value in solution.items():
        print(f"  {var}: {value}")
else:
    print("No se encontró solución.")