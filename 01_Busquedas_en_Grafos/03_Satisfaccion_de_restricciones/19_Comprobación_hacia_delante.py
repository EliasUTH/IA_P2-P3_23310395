class CSPForwardChecking:
    """
    Clase para resolver Problemas de Satisfacción de Restricciones (CSP)
    usando backtracking con comprobación hacia delante (forward checking).
    """

    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = {var: list(dom) for var, dom in domains.items()}  # Copia de dominios
        self.constraints = constraints
        self.original_domains = {var: list(dom) for var, dom in domains.items()}  # Para resetear

    def is_consistent(self, var, value, assignment):
        """Verifica consistencia con variables asignadas."""
        for (var1, var2, constraint) in self.constraints:
            if var1 == var and var2 in assignment:
                if not constraint(value, assignment[var2]):
                    return False
            if var2 == var and var1 in assignment:
                if not constraint(assignment[var1], value):
                    return False
        return True

    def forward_check(self, var, value, assignment):
        """Realiza comprobación hacia delante: reduce dominios de variables no asignadas."""
        reductions = {}
        for (var1, var2, constraint) in self.constraints:
            if var1 == var and var2 not in assignment:
                # Reducir dominio de var2
                original = self.domains[var2][:]
                self.domains[var2] = [v for v in self.domains[var2] if constraint(value, v)]
                if not self.domains[var2]:
                    # Dominio vacío, conflicto
                    return False, reductions
                reductions[var2] = original
            if var2 == var and var1 not in assignment:
                # Reducir dominio de var1
                original = self.domains[var1][:]
                self.domains[var1] = [v for v in self.domains[var1] if constraint(v, value)]
                if not self.domains[var1]:
                    return False, reductions
                reductions[var1] = original
        return True, reductions

    def undo_forward_check(self, reductions):
        """Deshace las reducciones de dominios."""
        for var, original in reductions.items():
            self.domains[var] = original

    def select_unassigned_variable(self, assignment):
        """Selecciona variable no asignada con dominio más pequeño (MRV)."""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def backtracking_search(self):
        """Inicia la búsqueda con backtracking y forward checking."""
        assignment = {}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in list(self.domains[var]):  # Copia para evitar modificaciones durante iteración
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                # Forward checking
                consistent, reductions = self.forward_check(var, value, assignment)
                if consistent:
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                # Undo forward checking
                self.undo_forward_check(reductions)
                del assignment[var]
        return None

# Ejemplo de uso: Coloreo de mapa
print("=== Comprobación Hacia Delante en CSP ===")
variables = ['A', 'B', 'C', 'D']
domains = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
constraints = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

csp = CSPForwardChecking(variables, domains, constraints)
solution = csp.backtracking_search()

if solution:
    print("Solución encontrada:")
    for var, value in solution.items():
        print(f"  {var}: {value}")
else:
    print("No se encontró solución.")