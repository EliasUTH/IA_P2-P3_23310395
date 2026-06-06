import math
import time


def dijkstra_simulador(grafo, inicio):
    """
    Simulador paso a paso del Algoritmo de Dijkstra.
    Encuentra la ruta más corta desde un nodo de inicio hacia todos los demás.
    """
    print("___INICIANDO SIMULADOR DE DIJKSTRA___")
    print(f"Nodo de origen: '{inicio}'")


    # 1. PREPARACIÓN
    # Inicializamos todas las distancias a "infinito" excepto la del nodo de inicio.
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[inicio] = 0
    
    # Diccionario para rastrear el camino (quién es el padre de cada nodo)
    padres = {nodo: None for nodo in grafo}
    
    # Lista de nodos que aún no hemos evaluado
    no_visitados = list(grafo.keys())
    paso = 1

    # 2. CICLO PRINCIPAL (El corazón de Dijkstra)
    while no_visitados:
        
        # Seleccionamos el nodo no visitado que tenga la distancia acumulada más pequeña.
        # (En el paso 1, siempre será el nodo 'inicio' porque su distancia es 0).
        nodo_actual = min(no_visitados, key=lambda nodo: distancias[nodo])
        
        # Si la distancia menor disponible es infinito, significa que los nodos 
        # restantes están desconectados del grafo. Terminamos prematuramente.
        if distancias[nodo_actual] == math.inf:
            print("Los nodos restantes son inalcanzables. Fin del algoritmo.")
            break
        print(f"___PASO {paso}___")
        print(f"Visitando nodo: '{nodo_actual}'")
        print(f"(Distancia acumulada desde el origen: {distancias[nodo_actual]})")
        

        # Marcamos el nodo como visitado sacándolo de la lista
        no_visitados.remove(nodo_actual)
        
        # Extraemos los vecinos del nodo actual
        vecinos = grafo[nodo_actual]
        
        # 3. ANÁLISIS DE VECINOS
        for vecino, peso_arista in vecinos.items():
            # Solo analizamos vecinos que aún no hayan sido visitados permanentemente
            if vecino in no_visitados:
                # Calculamos cuánto nos costaría llegar a este vecino pasando por el nodo actual
                distancia_tentativa = distancias[nodo_actual] + peso_arista
                print(f"Analizando ruta hacia vecino '{vecino}' (Peso arista: {peso_arista})")
                print(f"Distancia tentativa = {distancias[nodo_actual]} + {peso_arista} = {distancia_tentativa}")
                # Si encontramos un atajo (una ruta más barata), la actualizamos
                if distancia_tentativa < distancias[vecino]:
                    print(f"¡Mejor ruta encontrada! Se actualiza la distancia de '{vecino}' (Antes: {distancias[vecino]} -> Ahora: {distancia_tentativa}).")
                    distancias[vecino] = distancia_tentativa
                    padres[vecino] = nodo_actual
                else:
                    print(f"Ruta descartada. Ya conocemos un camino igual o más rápido hacia '{vecino}' (Actual: {distancias[vecino]}).")
        print(f"Tabla de distancias actualizadas: {distancias}")
        print("\n")
        
        # Pausa para que el usuario pueda leer la consola cómodamente
        time.sleep(1.5) 
        paso += 1
    print("___SIMULACIÓN TERMINADA___")
    return distancias, padres



# --- Ejecución de Prueba ---
# Construimos un grafo simulando un mapa de ciudades conectadas.
# Las letras son ciudades, los números son kilómetros de distancia.
mapa_ciudades = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
    'E': {'C': 10, 'D': 2, 'Z': 3},
    'Z': {'D': 6, 'E': 3}
}


# Ejecutamos el simulador iniciando desde la ciudad 'A'
distancias_finales, rastreo_rutas = dijkstra_simulador(mapa_ciudades, 'A')
# Mostramos el reporte final
print("\n REPORTE FINAL: Distancias mínimas desde 'A'")
for destino, distancia in distancias_finales.items():
    print(f"Ruta óptima hacia {destino}: {distancia} unidades de distancia.")