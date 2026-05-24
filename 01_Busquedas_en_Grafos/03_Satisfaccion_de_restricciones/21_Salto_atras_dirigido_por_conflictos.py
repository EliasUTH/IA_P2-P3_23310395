class CSPBackjumping:
    """
    Clase para resolver CSP con salto atrás dirigido por conflictos (conflict-directed backjumping).
    """

    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.conflicts = {var: set() for var in variables}  # Variables que causan conflictos

    def is_consistent(self, var, value, assignment):
        """Verifica consistencia con variables asignadas."""
        for (var1, var2, constraint) in self.constraints:
            if var1 == var and var2 in assignment:
                if not constraint(value, assignment[var2]):
                    self.conflicts[var].add(var2)
                    return False
            if var2 == var and var1 in assignment:
                if not constraint(assignment[var1], value):
                    self.conflicts[var].add(var1)
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        """Selecciona variable no asignada."""
        unassigned = [v for v in self.variables if v not in assignment]
        return unassigned[0] if unassigned else None

    def backjumping_search(self):
        """Inicia la búsqueda con backjumping."""
        assignment = {}
        return self.backjump(assignment)

    def backjump(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None

        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backjump(assignment)
                if result is not None:
                    return result
                # Backjumping: saltar a la variable que causó el conflicto
                if self.conflicts[var]:
                    jump_to = max(self.conflicts[var], key=lambda v: self.variables.index(v))
                    # Remover asignaciones hasta jump_to
                    vars_to_remove = []
                    for assigned_var in reversed(list(assignment.keys())):
                        if assigned_var == jump_to:
                            break
                        vars_to_remove.append(assigned_var)
                    for v in vars_to_remove:
                        del assignment[v]
                    # Limpiar conflictos
                    self.conflicts = {v: set() for v in self.variables}
                    return None  # Continuar desde jump_to
                del assignment[var]
        return None

# Ejemplo de uso: Coloreo de mapa
print("=== Salto Atrás Dirigido por Conflictos ===")
variables = ['A', 'B', 'C', 'D']
domains = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
constraints = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

csp = CSPBackjumping(variables, domains, constraints)
solution = csp.backjumping_search()

if solution:
    print("Solución encontrada:")
    for var, value in solution.items():
        print(f"  {var}: {value}")
else:
    print("No se encontró solución.")