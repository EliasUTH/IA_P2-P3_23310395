import itertools
print("=== EQUIVALENCIA, VALIDEZ Y SATISFACIBILIDAD ===\n")



# --- 1. MOTOR DE EVALUACIÓN DE MODELOS ---
def obtener_todos_los_modelos(variables):
    """Genera todos los mundos posibles (combinaciones V/F) para las variables dadas."""
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    # Retorna una lista de diccionarios, ej: [{'P': True, 'Q': True}, {'P': True, 'Q': False}...]
    return [dict(zip(variables, valores)) for valores in combinaciones]



# --- 2. DEFINICIÓN DE LAS PROPIEDADES LÓGICAS ---
def es_satisfacible(formula, variables):
    """
    SATISFACIBILIDAD: Una fórmula es satisfacible si existe AL MENOS UN modelo 
    (un mundo posible) donde la fórmula es Verdadera.
    """
    modelos = obtener_todos_los_modelos(variables)
    for m in modelos:
        if formula(**m):
            return True # Encontramos al menos un modelo que la hace verdad
    return False # Es una contradicción (insatisfacible)



def es_valida(formula, variables):
    """
    VALIDEZ (Tautología): Una fórmula es válida si es Verdadera en TODOS 
    los modelos posibles. No importa qué valores tengan las variables, siempre es cierta.
    """
    modelos = obtener_todos_los_modelos(variables)
    for m in modelos:
        if not formula(**m):
            return False # Encontramos un modelo donde falla, por tanto no es válida
    return True



def son_equivalentes(formula1, formula2, variables):
    """
    EQUIVALENCIA: Dos fórmulas son equivalentes si en TODOS los modelos posibles 
    tienen exactamente el mismo valor de verdad.
    """
    modelos = obtener_todos_los_modelos(variables)
    for m in modelos:
        if formula1(**m) != formula2(**m):
            return False # Difieren en al menos un escenario
    return True



# --- 3. PRUEBAS Y EJECUCIÓN ---
print("--- A. SATISFACIBILIDAD ---")
variables_a = ["P", "Q"]
# Fórmula: P AND Q
formula_sat = lambda P, Q: P and Q
# Fórmula: P AND (NOT P)
formula_insat = lambda P, Q: P and (not P)
print(f"¿'P AND Q' es satisfacible?      -> {'SÍ' if es_satisfacible(formula_sat, variables_a) else 'NO'}")
print(f"¿'P AND (NOT P)' es satisfacible? -> {'SÍ' if es_satisfacible(formula_insat, variables_a) else 'NO (Contradicción)'}")



print("\n--- B. VALIDEZ (TAUTOLOGÍA) ---")
variables_b = ["P"]
# Fórmula: P OR (NOT P) - Ley del tercero excluido
formula_valida = lambda P: P or (not P)
print(f"¿'P OR (NOT P)' es válida?        -> {'SÍ (Tautología)' if es_valida(formula_valida, variables_b) else 'NO'}")
print(f"¿'P AND (NOT P)' es válida?       -> {'SÍ' if es_valida(lambda P: P and (not P), variables_b) else 'NO'}")



print("\n--- C. EQUIVALENCIA (Leyes de De Morgan) ---")
variables_c = ["P", "Q"]
# Fórmula 1: NOT (P AND Q)
f1 = lambda P, Q: not (P and Q)
# Fórmula 2: (NOT P) OR (NOT Q)
f2 = lambda P, Q: (not P) or (not Q)
print("Comparando: NOT(P AND Q) con (NOT P) OR (NOT Q)")
print(f"¿Son equivalentes? -> {'SÍ' if son_equivalentes(f1, f2, variables_c) else 'NO'}")



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. SATISFACIBILIDAD: El algoritmo se detiene (retorna True) en cuanto encuentra el primer éxito (Cortocircuito).")
print("2. VALIDEZ: Está estrechamente ligada a la satisfacibilidad. Una fórmula es válida si su negación es insatisfacible.")
print("3. EQUIVALENCIA: Dos fórmulas son equivalentes si la expresión (F1 <=> F2) es Válida.")