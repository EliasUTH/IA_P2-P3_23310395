from collections import deque

def revise(domains, var1, var2, constraint):
    """
    Revisa el dominio de var1 para que sea consistente con var2 bajo la restricción.
    Retorna True si se hizo algún cambio.
    """
    revised = False
    to_remove = []
    for value1 in domains[var1]:
        # Verifica si hay al menos un valor en var2 que satisfaga la restricción
        if not any(constraint(value1, value2) for value2 in domains[var2]):
            to_remove.append(value1)
            revised = True
    for value in to_remove:
        domains[var1].remove(value)
    return revised

def ac3(domains, constraints):
    """
    Algoritmo AC-3 para propagación de restricciones (arc consistency).
    Reduce dominios para que sean consistentes con restricciones binarias.

    Parámetros:
    - domains: diccionario {variable: lista de valores}
    - constraints: lista de tuplas (var1, var2, función_restricción)

    Retorna: True si los dominios son consistentes, False si hay dominio vacío.
    """
    # Cola de arcos: cada restricción genera dos arcos (var1->var2 y var2->var1)
    queue = deque()
    for var1, var2, _ in constraints:
        queue.append((var1, var2))
        queue.append((var2, var1))

    while queue:
        var1, var2 = queue.popleft()
        # Encuentra la restricción correspondiente
        constraint = None
        for v1, v2, cons in constraints:
            if (v1 == var1 and v2 == var2) or (v1 == var2 and v2 == var1):
                constraint = cons
                break
        if constraint is None:
            continue

        if revise(domains, var1, var2, constraint):
            if not domains[var1]:
                return False  # Dominio vacío, inconsistente
            # Agregar arcos entrantes a la cola
            for other_var, _, _ in constraints:
                if other_var != var2 and (other_var == var1 or (var1, other_var) in [(v1, v2) for v1, v2, _ in constraints]):
                    queue.append((other_var, var1))

    return True

# Ejemplo de uso: Coloreo de mapa con propagación
print("=== Propagación de Restricciones (AC-3) ===")
variables = ['A', 'B', 'C', 'D']
domains = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
constraints = [
    ('A', 'B', lambda x, y: x != y),
    ('A', 'C', lambda x, y: x != y),
    ('B', 'C', lambda x, y: x != y),
    ('B', 'D', lambda x, y: x != y),
    ('C', 'D', lambda x, y: x != y),
]

print("Dominios antes de AC-3:")
for var, dom in domains.items():
    print(f"  {var}: {dom}")

if ac3(domains, constraints):
    print("Dominios después de AC-3 (consistentes):")
    for var, dom in domains.items():
        print(f"  {var}: {dom}")
    print("Los dominios son consistentes. Ahora puedes usar backtracking.")
else:
    print("Los dominios son inconsistentes (dominio vacío).")