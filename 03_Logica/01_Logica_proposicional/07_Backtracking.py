print("=== ALGORITMO DE BACKTRACKING (VUELTA ATRÁS) ===\n")
# --- 1. DEFINICIÓN DEL PROBLEMA (Grafo y Dominio) ---
# Representamos un mapa simplificado (ej. estados de un país) y sus fronteras.
# Las claves son las regiones, los valores son sus vecinos.
vecinos = {
    "Norte": ["Centro", "Este", "Oeste"],
    "Centro": ["Norte", "Sur", "Este", "Oeste"], # El Centro toca a todos
    "Sur": ["Centro", "Este", "Oeste"],
    "Este": ["Norte", "Centro", "Sur"],
    "Oeste": ["Norte", "Centro", "Sur"]
}



# El "Dominio" son los valores válidos para cada variable
colores_disponibles = ["Rojo", "Verde", "Azul"]




# --- 2. FUNCIÓN DE RESTRICCIÓN ---
def es_asignacion_valida(region, color, asignacion_actual):
    """
    Verifica si asignar 'color' a 'region' viola alguna regla.
    La regla es: Ningún vecino puede tener el mismo color.
    """
    for vecino in vecinos[region]:
        # Si el vecino ya tiene color y es el mismo que queremos usar, es inválido
        if vecino in asignacion_actual and asignacion_actual[vecino] == color:
            return False
    return True



# --- 3. MOTOR DE BACKTRACKING RECURSIVO ---
def resolver_backtracking(asignacion_actual, variables_restantes, nivel=0):
    indent = "  " * nivel
    


    # Caso Base: Si ya no hay variables restantes, ¡hemos resuelto el problema!
    if not variables_restantes:
        return asignacion_actual
    # Seleccionamos la siguiente región a colorear
    region_actual = variables_restantes[0]
    print(f"{indent}[+] Intentando colorear: {region_actual}")
    # Probamos cada color disponible
    for color in colores_disponibles:
        print(f"{indent}  -> Probando color: {color} en {region_actual}")
        if es_asignacion_valida(region_actual, color, asignacion_actual):
            # Si es válido, hacemos la asignación temporal
            asignacion_actual[region_actual] = color
            nuevas_restantes = variables_restantes[1:]
            


            # Llamada recursiva para colorear el resto del mapa
            resultado = resolver_backtracking(asignacion_actual, nuevas_restantes, nivel + 1)
            # Si el resultado no es falso, encontramos la solución completa
            if resultado is not False:
                return resultado



            # --- EL CORAZÓN DEL BACKTRACKING ---
            # Si llegamos aquí, significa que la asignación actual llevó a un callejón
            # sin salida más adelante. Deshacemos la asignación y probamos el siguiente color.
            print(f"{indent}  [!] Callejón sin salida. HACIENDO BACKTRACK en {region_actual} (quitando {color})")
            del asignacion_actual[region_actual]
        else:
            print(f"{indent}  [x] Conflicto: {color} ya está usado por un vecino de {region_actual}")



    # Si probamos todos los colores y ninguno funciona, esta rama entera es un fracaso
    return False



# --- 4. EJECUCIÓN ---
print("Iniciando motor de resolución de restricciones...\n")
lista_regiones = list(vecinos.keys()) # ["Norte", "Centro", "Sur", "Este", "Oeste"]
solucion = resolver_backtracking({}, lista_regiones)
print("\n" + "="*45)
if solucion:
    print("¡SOLUCIÓN ENCONTRADA!")
    for region, color in solucion.items():
        print(f"- {region}: {color}")
else:
    print("El problema no tiene solución con los colores dados.")
print("="*45)



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Poda de Ramas (Pruning): A diferencia de la fuerza bruta (que generaría 3^5 = 243")
print("   combinaciones a ciegas), el backtracking descarta combinaciones inválidas instantáneamente.")
print("2. Restricciones Dinámicas: La función 'es_asignacion_valida' actúa como el juez")
print("   en cada nodo del árbol de búsqueda.")
print("3. Retroceso de Estado: El comando 'del asignacion_actual[region]' es vital;")
print("   limpia la memoria del error para intentar un camino nuevo.")