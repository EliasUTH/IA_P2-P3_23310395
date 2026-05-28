import random
print("=== BÚSQUEDA LOCAL: ASCENSO DE COLINAS (HILL CLIMBING) ===\n")



# --- 1. CONFIGURACIÓN DEL PROBLEMA ---
# Representamos el tablero como una lista. 
# El índice es la columna, el valor es la fila de la reina.
# Ejemplo: tablero[0] = 2 significa que en la columna 0, la reina está en la fila 2.
N_REINAS = 5




def calcular_conflictos(tablero):
    """
    Función Heurística (Costo): Cuenta cuántos pares de reinas se están atacando.
    Un costo de 0 significa que el problema está resuelto.
    """
    ataques = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            fila_i = tablero[i]
            fila_j = tablero[j]
            
            # Se atacan si están en la misma fila
            if fila_i == fila_j:
                ataques += 1
            # Se atacan si están en la misma diagonal (diferencia de filas == diferencia de columnas)
            elif abs(fila_i - fila_j) == abs(i - j):
                ataques += 1
    return ataques



def obtener_mejores_vecinos(tablero):
    """
    Genera todos los tableros vecinos (moviendo una reina en su columna)
    y devuelve los que tengan el menor número de conflictos.
    """
    mejor_costo = float('inf')
    mejores_vecinos = []
    n = len(tablero)
    


    for columna in range(n):
        fila_actual = tablero[columna]
        for nueva_fila in range(n):
            if nueva_fila != fila_actual:
                # Clonar tablero y mover la reina
                vecino = list(tablero)
                vecino[columna] = nueva_fila
                costo_vecino = calcular_conflictos(vecino)
                if costo_vecino < mejor_costo:
                    mejor_costo = costo_vecino
                    mejores_vecinos = [vecino]
                elif costo_vecino == mejor_costo:
                    mejores_vecinos.append(vecino)   
    return mejores_vecinos, mejor_costo



def imprimir_tablero(tablero):
    """Renderiza el estado actual en consola."""
    n = len(tablero)
    for fila in range(n):
        linea = ""
        for col in range(n):
            if tablero[col] == fila:
                linea += "[Q]"
            else:
                linea += "[ ]"
        print(linea)
    print(f"Costo (Ataques): {calcular_conflictos(tablero)}\n")



# --- 2. MOTOR DE ASCENSO DE COLINAS ---
def ascenso_colinas(tablero_inicial):
    estado_actual = tablero_inicial
    costo_actual = calcular_conflictos(estado_actual)
    iteracion = 1
    print(f"--- ESTADO INICIAL ---")
    imprimir_tablero(estado_actual)
    


    while True:
        # Obtenemos los vecinos que mejoran la situación
        mejores_vecinos, costo_vecinos = obtener_mejores_vecinos(estado_actual)
        # Condición de parada (Óptimo Local o Global)
        # Si ningún vecino es mejor que mi estado actual, dejo de buscar.
        if costo_vecinos >= costo_actual:
            if costo_actual == 0:
                print("¡Óptimo Global alcanzado! Solución perfecta.")
            else:
                print("¡Atascado en un Óptimo Local! No hay movimiento que mejore el costo.")
            return estado_actual
        # Nos movemos al mejor vecino (elegimos uno al azar si hay empate)
        estado_actual = random.choice(mejores_vecinos)
        costo_actual = costo_vecinos
        print(f"--- ITERACIÓN {iteracion} ---")
        imprimir_tablero(estado_actual)
        iteracion += 1



# --- 3. EJECUCIÓN ---
# Fijamos la semilla aleatoria para que el resultado sea siempre el mismo en tu consola
random.seed(42)



# Tablero inicial aleatorio
estado_arranque = [random.randint(0, N_REINAS - 1) for _ in range(N_REINAS)]
estado_final = ascenso_colinas(estado_arranque)



print("=== ANÁLISIS TÉCNICO ===")
print("1. Eficiencia de Memoria: A diferencia de BFS o DFS, este algoritmo no guarda un árbol de estados. Su complejidad espacial es constante O(1).")
print("2. Función Heurística: Es el 'radar' que guía al algoritmo (calcular_conflictos). Siempre buscará minimizar este número.")
print("3. Ceguera (Miopía): Si el algoritmo llega a un punto donde mover cualquier reina empeora la situación, se detiene, incluso si a dos pasos de distancia hay una solución perfecta (Óptimo Local).")