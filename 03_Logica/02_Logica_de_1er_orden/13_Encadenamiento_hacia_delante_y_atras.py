print("=== FOL: ENCADENAMIENTO HACIA ADELANTE Y ATRÁS ===\n")
# --- 1. MOTOR DE UNIFICACIÓN BÁSICO ---
# (Versión compacta del módulo anterior para que el script sea independiente)


def es_variable(x):
    return isinstance(x, str) and x.islower()


def unificar_var(var, val, theta):
    if var in theta: return unificar(theta[var], val, theta)
    if es_variable(val) and val in theta: return unificar(var, theta[val], theta)
    theta_nueva = theta.copy()
    theta_nueva[var] = val
    return theta_nueva


def unificar(x, y, theta):
    if theta is None: return None
    if x == y: return theta
    if es_variable(x): return unificar_var(x, y, theta)
    if es_variable(y): return unificar_var(y, x, theta)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        return unificar(x[1:], y[1:], unificar(x[0], y[0], theta))
    return None


def aplicar_sustitucion(termino, theta):
    """Reemplaza las variables en un término usando el diccionario theta."""
    if es_variable(termino):
        # Si la variable está en theta, buscamos su valor recursivamente
        return aplicar_sustitucion(theta[termino], theta) if termino in theta else termino
    elif isinstance(termino, tuple):
        # Si es un predicado, aplicamos sustitución a todos sus elementos
        return tuple(aplicar_sustitucion(arg, theta) for arg in termino)
    return termino


# --- 2. BASE DE CONOCIMIENTO (FOL) ---
# Hechos base (sin variables)
hechos = {
    ("Rey", "Juan"),
    ("Avaro", "Juan"),
    ("Padre", "Juan", "Ricardo")
}


# Reglas: (Lista de premisas, Conclusión)
reglas = [
    # Regla 1: Todo Rey que es Avaro es Malvado. ∀x (Rey(x) ∧ Avaro(x) ⇒ Malvado(x))
    ([("Rey", "x"), ("Avaro", "x")], ("Malvado", "x")),
    
    # Regla 2: Todo Malvado es Peligroso. ∀y (Malvado(y) ⇒ Peligroso(y))
    ([("Malvado", "y")], ("Peligroso", "y"))
]



# --- 3. ENCADENAMIENTO HACIA ADELANTE (Forward Chaining) ---
def buscar_sustituciones(premisas, hechos, theta_actual=None):
    """Evalúa recursivamente si un conjunto de premisas se cumple en los hechos."""
    if theta_actual is None: theta_actual = {}
    if not premisas:
        return [theta_actual] # Éxito, devolvemos la sustitución encontrada
    premisa_actual = aplicar_sustitucion(premisas[0], theta_actual)
    resultados = []
    for hecho in hechos:
        # Intentamos unificar la premisa actual con algún hecho de la base de datos
        theta_nueva = unificar(premisa_actual, hecho, theta_actual)
        if theta_nueva is not None:
            # Si unifica, procedemos con las premisas restantes usando la nueva sustitución
            sustituciones_restantes = buscar_sustituciones(premisas[1:], hechos, theta_nueva)
            resultados.extend(sustituciones_restantes)
    return resultados



def encadenamiento_hacia_adelante_fol(reglas, hechos_iniciales):
    print("\n[FORWARD CHAINING] Iniciando ciclo de inferencia guiado por datos...")
    hechos_conocidos = set(hechos_iniciales)
    nuevos_hechos_generados = True
    while nuevos_hechos_generados:
        nuevos_hechos_generados = False
        

        for premisas, conclusion in reglas:
            # Buscamos todas las combinaciones de variables que hacen ciertas las premisas
            sustituciones = buscar_sustituciones(premisas, hechos_conocidos)
            

            for theta in sustituciones:
                # Instanciamos la conclusión con las variables encontradas
                nuevo_hecho = aplicar_sustitucion(conclusion, theta)
                

                if nuevo_hecho not in hechos_conocidos:
                    print(f" -> DEDUCCIÓN: Aplicando theta {theta} a la regla.")
                    print(f"    Agregando nuevo hecho: {nuevo_hecho}")
                    hechos_conocidos.add(nuevo_hecho)
                    nuevos_hechos_generados = True
    return hechos_conocidos


# --- 4. ENCADENAMIENTO HACIA ATRÁS (Backward Chaining) ---
def encadenamiento_hacia_atras_fol(objetivo, reglas, hechos, theta=None, nivel=0):
    indent = "  " * nivel
    if theta is None: theta = {}
    objetivo_instanciado = aplicar_sustitucion(objetivo, theta)
    print(f"{indent}[BACKWARD] Buscando probar: {objetivo_instanciado}")
    


    # 1. Comprobar si el objetivo unifica directamente con un hecho conocido
    for hecho in hechos:
        theta_nueva = unificar(objetivo_instanciado, hecho, theta)
        if theta_nueva is not None:
            print(f"{indent} -> ¡Hecho encontrado! Sustitución: {theta_nueva}")
            yield theta_nueva # Usamos generadores (yield) por si hay múltiples caminos


    # 2. Comprobar si el objetivo unifica con la conclusión de alguna regla
    for premisas, conclusion in reglas:
        theta_regla = unificar(objetivo_instanciado, conclusion, theta)
        if theta_regla is not None:
            print(f"{indent} -> Unifica con la regla que concluye en: {conclusion}")
            

            # Intentar probar todas las premisas de esta regla
            # (Simplificamos usando una lista recursiva de generadores)
            def probar_premisas(lista_premisas, theta_actual, nivel_actual):
                if not lista_premisas:
                    yield theta_actual
                else:
                    for t_parcial in encadenamiento_hacia_atras_fol(lista_premisas[0], reglas, hechos, theta_actual, nivel_actual + 1):
                        yield from probar_premisas(lista_premisas[1:], t_parcial, nivel_actual)
            yield from probar_premisas(premisas, theta_regla, nivel)


# --- 5. EJECUCIÓN ---
print("--- PRUEBA 1: HACIA ADELANTE ---")
base_final = encadenamiento_hacia_adelante_fol(reglas, hechos)
print("\nBase de Conocimiento Final:")
for h in base_final: print(f" - {h}")
print("\n" + "="*50 + "\n")
print("--- PRUEBA 2: HACIA ATRÁS ---")
meta = ("Peligroso", "Juan")
print(f"Objetivo: ¿Es cierto que {meta}?")


generador_soluciones = encadenamiento_hacia_atras_fol(meta, reglas, hechos)
soluciones = list(generador_soluciones)


if soluciones:
    print(f"\n¡ÉXITO! El objetivo es derivable. Entornos resultantes: {soluciones}")
else:
    print("\nFALLO. No se pudo derivar el objetivo.")


print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Modus Ponens Generalizado: Al combinar reglas lógicas con unificación, el sistema aplica la regla ∀x (P(x) => Q(x)) directamente a la constante 'Juan'.")
print("2. Generadores (yield): En Backward Chaining, usamos generadores nativos de Python. Esto permite al motor explorar múltiples caminos lógicos y retroceder (backtrack) si un hilo de pensamiento falla, sin bloquear la memoria.")