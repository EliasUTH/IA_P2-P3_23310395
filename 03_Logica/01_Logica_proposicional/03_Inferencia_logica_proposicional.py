print("=== INFERENCIA LÓGICA: VERIFICACIÓN DE MODELOS (TT-ENTAILS) ===\n")


# --- 1. MOTOR DE INFERENCIA RECURSIVO ---
def verificar_todos_los_modelos(kb, consulta, simbolos, modelo_actual):
    """
    Recorre recursivamente todas las combinaciones de Verdadero/Falso.
    """
    # Caso base: Si ya asignamos valores a todas las variables
    if not simbolos:
        # Si la Base de Conocimiento es cierta en este mundo hipotético...
        if kb(modelo_actual):
            # ...entonces la Consulta DEBE ser cierta para que la inferencia sea válida.
            return consulta(modelo_actual)
        else:
            # Si la KB es falsa en este mundo, este mundo es irrelevante.
            # (Principio de Verdad Vacua: Falso implica cualquier cosa)
            return True
    else:
        # Paso recursivo: Tomamos el primer símbolo de la lista de variables pendientes
        P = simbolos[0]
        resto_simbolos = simbolos[1:]
        # Bifurcación: Creamos dos mundos posibles
        # Mundo 1: Asumimos que P es Verdadero
        modelo_verdadero = modelo_actual.copy()
        modelo_verdadero[P] = True
        # Mundo 2: Asumimos que P es Falso
        modelo_falso = modelo_actual.copy()
        modelo_falso[P] = False
        # Para que la inferencia sea válida, DEBE cumplirse en ambos ramales
        return (verificar_todos_los_modelos(kb, consulta, resto_simbolos, modelo_verdadero) and 
                verificar_todos_los_modelos(kb, consulta, resto_simbolos, modelo_falso))



def inferir(kb, consulta, simbolos):
    """Punto de entrada para el algoritmo de inferencia."""
    return verificar_todos_los_modelos(kb, consulta, simbolos, {})



# --- 2. DEFINICIÓN DEL ESCENARIO ---
# Símbolos (Variables proposicionales)
variables = ["LLUEVE", "CALLE_MOJADA"]



# Base de Conocimiento (KB):
# Regla 1: Si llueve, la calle está mojada. (LLUEVE => CALLE_MOJADA)
# Regla 2: Llueve. (LLUEVE es Verdadero)
def base_de_conocimiento(modelo):
    # La implicación (A => B) es equivalente a (not A or B)
    regla_1 = (not modelo["LLUEVE"]) or modelo["CALLE_MOJADA"]
    regla_2 = modelo["LLUEVE"]
    # La KB es la conjunción (AND) de todos sus hechos y reglas
    return regla_1 and regla_2



# --- 3. PRUEBAS DE INFERENCIA ---
print("Escenario:")
print(" - Regla: Si llueve, entonces la calle está mojada.")
print(" - Hecho: Está lloviendo.")
print("-" * 50)



# Consulta A: ¿Podemos inferir que la calle está mojada?
consulta_a = lambda modelo: modelo["CALLE_MOJADA"]
resultado_a = inferir(base_de_conocimiento, consulta_a, variables)
print(f"Consulta A: ¿La calle está mojada? -> {'SÍ (Válido)' if resultado_a else 'NO (Inválido)'}")



# Consulta B: ¿Podemos inferir que NO está lloviendo? (Para probar un caso falso)
consulta_b = lambda modelo: not modelo["LLUEVE"]
resultado_b = inferir(base_de_conocimiento, consulta_b, variables)
print(f"Consulta B: ¿No está lloviendo?    -> {'SÍ (Válido)' if resultado_b else 'NO (Inválido)'}")



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. TT-Entails (Truth Table Entailment): El algoritmo evalúa matemáticamente")
print("   que los modelos de la KB sean un subconjunto de los modelos de la Consulta.")
print("2. Recursividad (Árbol de Búsqueda): Se ramifica creando entornos paralelos.")
print("3. Inferencia Estricta: Si un solo modelo hace la KB Verdadera y la")
print("   Consulta Falsa, la inferencia devuelve False y rechaza el argumento.")