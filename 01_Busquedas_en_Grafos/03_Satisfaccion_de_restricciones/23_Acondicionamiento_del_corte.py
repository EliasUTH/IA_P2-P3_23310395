class CSPConditioningCut:
    """
    Clase para resolver CSP usando acondicionamiento del corte (conditioning cut).
    Técnica que acondiciona el problema en base a asignaciones parciales
    y usa cortes (prunning) para eliminar ramas infeasibles tempranamente.
    """

    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.original_domains = {var: list(dom) for var, dom in domains.items()}
        self.domains = {var: list(dom) for var, dom in domains.items()}
        self.constraints = constraints
        self.cuts_applied = 0

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

    def apply_cut(self, var, value, assignment):
        """
        Aplica un corte: condiciona los dominios de variables futuras
        basándose en la asignación actual de var=value.
        Retorna los cambios realizados para poder deshacerlos.
        """
        changes = {}
        for (var1, var2, constraint) in self.constraints:
            # Si var1==var, condiciona var2
            if var1 == var and var2 not in assignment:
                original = self.domains[var2][:]
                self.domains[var2] = [v for v in self.domains[var2] if constraint(value, v)]
                if self.domains[var2] != original:
                    changes[var2] = original
                    self.cuts_applied += 1

            # Si var2==var, condiciona var1
            if var2 == var and var1 not in assignment:
                original = self.domains[var1][:]
                self.domains[var1] = [v for v in self.domains[var1] if constraint(v, value)]
                if self.domains[var1] != original:
                    changes[var1] = original
                    self.cuts_applied += 1

        return changes

    def undo_cut(self, changes):
        """Deshace los cambios realizados por un corte."""
        for var, original in changes.items():
            self.domains[var] = original

    def select_unassigned_variable(self, assignment):
        """Selecciona variable con dominio más pequeño (MRV)."""
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def conditioning_cut_search(self):
        """Inicia la búsqueda con acondicionamiento del corte."""
        assignment = {}
        return self.search(assignment)

    def search(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None

        for value in list(self.domains[var]):  # Copia del dominio
            if self.is_consistent(var, value, assignment):
                assignment[var] = value

                # Aplicar corte: condicionar dominios
                changes = self.apply_cut(var, value, assignment)

                # Verificar que no haya dominio vacío después del corte
                if all(len(self.domains[v]) > 0 for v in self.variables if v not in assignment):
                    result = self.search(assignment)
                    if result is not None:
                        return result

                # Deshacer corte y backtrack
                self.undo_cut(changes)
                del assignment[var]

        return None

# Ejemplo de uso: Coloreo de mapa
print("=== Acondicionamiento del Corte en CSP ===")
variables = ['A', 'B', 'C', 'D']
domains = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
constraints = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

csp = CSPConditioningCut(variables, domains, constraints)
solution = csp.conditioning_cut_search()

if solution:
    print("Solución encontrada:")
    for var, value in solution.items():
        print(f"  {var}: {value}")
    print(f"Cortes aplicados: {csp.cuts_applied}")
else:
    print("No se encontró solución.")