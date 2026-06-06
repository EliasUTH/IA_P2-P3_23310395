import time

def prim_simulador(grafo, nodo_inicio):
    """
    Simulador paso a paso del Algoritmo de Prim.
    Encuentra la forma más barata de conectar TODOS los nodos de un grafo.
    """

    print("___INICIANDO SIMULADOR DE PRIM (Árbol de Expansión Mínima)___")
    print(f"Nodo raíz de inicio: '{nodo_inicio}'")


    # 1. PREPARACIÓN
    visitados = set([nodo_inicio]) # Nodos que ya pertenecen a nuestro árbol
    nodos_totales = set(grafo.keys())
    
    arbol_minimo = [] # Aquí guardaremos las aristas (conexiones) definitivas
    costo_total = 0
    paso = 1

    # 2. CICLO PRINCIPAL (Crecer el árbol hasta cubrir todo el mapa)
    while visitados != nodos_totales:
        print(f"___PASO {paso}___")
        print(f"Nodos ya conectados en la red: {list(visitados)}")
        print("Buscando la conexión más barata hacia el 'mundo exterior'...")
        
        arista_mas_barata = None
        peso_minimo = float('inf')
        
        # 3. BÚSQUEDA ÁVIDA (Greedy)
        # Revisamos todos los nodos que ya están en nuestro árbol
        for nodo_visitado in visitados:
            # Revisamos hacia dónde se pueden conectar
            for vecino, peso in grafo[nodo_visitado].items():
                # Solo nos interesan conexiones a nodos que AÚN NO estén en el árbol
                if vecino not in visitados:
                    # Si esta opción es la más barata hasta ahora, la recordamos
                    if peso < peso_minimo:
                        peso_minimo = peso
                        arista_mas_barata = (nodo_visitado, vecino, peso)
        
        # 4. EXPANSIÓN DEL ÁRBOL
        origen, destino, costo = arista_mas_barata
        
        print(f"¡Conexión óptima encontrada! ")
        print(f"Uniendo rama '{origen}' con nuevo nodo '{destino}' (Costo: {costo}).")
        
        # Agregamos el nuevo nodo y la conexión a nuestros registros
        visitados.add(destino)
        arbol_minimo.append(arista_mas_barata)
        costo_total += costo
        
        print(f"Costo total de materiales/distancia hasta ahora: {costo_total}")
        print("\n")
        
        # Pausa de 1.5 segundos para facilitar la lectura
        time.sleep(1.5)
        paso += 1

    print("___SIMULACIÓN TERMINADA: RED GLOBAL CONECTADA___")
    print(f"Costo total óptimo del proyecto: {costo_total} unidades.")

    
    return arbol_minimo

# --- Ejecución de Prueba ---

# Usaremos el mismo mapa de ciudades que en Dijkstra para que veas la diferencia.
# Las letras son nodos (ej. casas), los números son el costo de conectarlos.
red_nodos = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
    'E': {'C': 10, 'D': 2, 'Z': 3},
    'Z': {'D': 6, 'E': 3}
}

# Ejecutamos el simulador iniciando desde 'A'
conexiones_finales = prim_simulador(red_nodos, 'A')

print("\nREPORTE FINAL DE CONSTRUCCIÓN:")
for origen, destino, costo in conexiones_finales:
    print(f"Construir cable/camino entre {origen} y {destino} (Costo: {costo})")