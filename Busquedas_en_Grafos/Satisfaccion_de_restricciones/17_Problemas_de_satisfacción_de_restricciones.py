class CSP:
    """
    Clase para representar un Problema de Satisfacción de Restricciones (CSP).
    """

    def __init__(self, variables, domains, constraints):
        """
        Parámetros:
        - variables: lista de variables
        - domains: diccionario {variable: lista de valores posibles}
        - constraints: lista de tuplas (var1, var2, función_restricción)
        """
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def is_consistent(self, var, value, assignment):
        """
        Verifica si asignar 'value' a 'var' es consistente con la asignación actual.
        """
        for (var1, var2, constraint) in self.constraints:
            if var1 == var:
                if var2 in assignment:
                    if not constraint(value, assignment[var2]):
                        return False
            elif var2 == var:
                if var1 in assignment:
                    if not constraint(assignment[var1], value):
                        return False
        return True

    def select_unassigned_variable(self, assignment):
        """
        Selecciona la siguiente variable no asignada.
        Estrategia: Minimum Remaining Values (MRV) - variable con menor dominio.
        """
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None
        # MRV: elegir variable con dominio más pequeño
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def backtracking_search(self):
        """
        Resuelve el CSP usando búsqueda con backtracking.
        """
        assignment = {}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """
        Función recursiva de backtracking.
        """
        # Si todas las variables están asignadas, solución encontrada
        if len(assignment) == len(self.variables):
            return assignment

        # Seleccionar variable no asignada
        var = self.select_unassigned_variable(assignment)

        # Intentar cada valor en el dominio
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                # Asignar valor
                assignment[var] = value

                # Recursión
                result = self.backtrack(assignment)
                if result is not None:
                    return result

                # Backtrack
                del assignment[var]

        return None

# Ejemplo 1: Problema de Coloreo de Mapas (Map Coloring)
print("=== Problema de Coloreo de Mapas ===")

# Variables: regiones (A, B, C, D)
variables_map = ['A', 'B', 'C', 'D']

# Dominios: colores disponibles
domains_map = {v: ['Rojo', 'Verde', 'Azul'] for v in variables_map}

# Restricciones: regiones adyacentes no pueden tener el mismo color
constraints_map = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

csp_map = CSP(variables_map, domains_map, constraints_map)
solution_map = csp_map.backtracking_search()

if solution_map:
    print("Solución encontrada:")
    for region, color in solution_map.items():
        print(f"  {region}: {color}")
else:
    print("No se encontró solución.")

# Ejemplo 2: Problema de las N-Reinas (N-Queens) simplificado para 4 reinas
print("\n=== Problema de las 4-Reinas ===")

# Variables: reinas (Q1, Q2, Q3, Q4)
n = 4
variables_queens = [f'Q{i}' for i in range(1, n+1)]

# Dominios: columnas (0 a 3)
domains_queens = {v: list(range(n)) for v in variables_queens}

# Restricciones: no atacarse mutuamente
def queens_constraint(col1, col2, row1, row2):
    """
    Verifica si dos reinas no se atacan.
    col1, col2: columnas de las reinas
    row1, row2: filas (indices de reinas)
    """
    return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)

constraints_queens = []
for i in range(n):
    for j in range(i+1, n):
        var1 = f'Q{i+1}'
        var2 = f'Q{j+1}'
        constraints_queens.append((var1, var2, lambda x, y, i=i, j=j: queens_constraint(x, y, i, j)))

csp_queens = CSP(variables_queens, domains_queens, constraints_queens)
solution_queens = csp_queens.backtracking_search()

if solution_queens:
    print("Solución encontrada (columna para cada reina):")
    for queen in sorted(solution_queens.keys()):
        print(f"  {queen}: columna {solution_queens[queen]}")
else:
    print("No se encontró solución.")