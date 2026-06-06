import time

# 1. Estructura Union-Find para detectar ciclos mágicamente
class UnionFind:
    def __init__(self, nodos):
        # Al principio, cada nodo es su propio jefe (padre)
        self.padre = {nodo: nodo for nodo in nodos}
        self.rango = {nodo: 0 for nodo in nodos}

    def encontrar(self, nodo):
        # Busca quién es el jefe supremo de este grupo
        if self.padre[nodo] == nodo:
            return nodo
        # Compresión de caminos (optimización)
        self.padre[nodo] = self.encontrar(self.padre[nodo])
        return self.padre[nodo]

    def unir(self, nodo1, nodo2):
        # Une dos grupos. Devuelve True si se unieron, False si ya estaban en el mismo grupo.
        raiz1 = self.encontrar(nodo1)
        raiz2 = self.encontrar(nodo2)

        if raiz1 != raiz2:
            # El grupo más grande absorbe al más pequeño
            if self.rango[raiz1] > self.rango[raiz2]:
                self.padre[raiz2] = raiz1
            elif self.rango[raiz1] < self.rango[raiz2]:
                self.padre[raiz1] = raiz2
            else:
                self.padre[raiz2] = raiz1
                self.rango[raiz1] += 1
            return True
        return False # ¡Forman un ciclo!

# 2. Algoritmo principal de Kruskal
def kruskal_simulador(aristas, nodos, modo="minimo"):
    """
    Simulador paso a paso del Algoritmo de Kruskal.
    modo: "minimo" (busca lo más barato) o "maximo" (busca lo más caro/ancho de banda)
    """
    print(f"___INICIANDO SIMULADOR DE KRUSKAL (Árbol de Coste {modo.upper()})___")

    # Si buscamos el mínimo, ordenamos de menor a mayor costo.
    # Si buscamos el máximo, ordenamos de mayor a menor costo (reversa).
    reverso = True if modo == "maximo" else False
    aristas_ordenadas = sorted(aristas, key=lambda item: item[2], reverse=reverso)
    
    uf = UnionFind(nodos)
    arbol_resultante = []
    costo_total = 0
    paso = 1

    print("Lista de aristas ordenadas por evaluación:")
    for a in aristas_ordenadas:
        print(f"   {a[0]} -- {a[1]} : {a[2]}")
    print("\n")
    time.sleep(2)

    # 3. CICLO PRINCIPAL
    for origen, destino, peso in aristas_ordenadas:
        print(f"___PASO {paso}___")
        print(f"Evaluando conexión: '{origen}' -- '{destino}' (Peso: {peso})")
        
        # Intentamos unir los nodos. Si devuelve True, no hay ciclo.
        if uf.unir(origen, destino):
            print(f"¡Conexión aceptada! No forma ciclos.")
            arbol_resultante.append((origen, destino, peso))
            costo_total += peso
        else:
            print(f"¡Conexión rechazada! Los nodos '{origen}' y '{destino}' ya estaban conectados por otra ruta (forman un ciclo).")
        
        print(f"Costo total acumulado: {costo_total}")
        print("\n")
        time.sleep(1.5)
        paso += 1
        
        # Optimización: Un árbol de expansión siempre tiene (N - 1) aristas.
        if len(arbol_resultante) == len(nodos) - 1:
            print("Se han conectado todos los nodos. Podemos detenernos temprano.")
            break

    print(f"SIMULACIÓN TERMINADA: RED GLOBAL CONECTADA ({modo.upper()})")
    print(f"Costo total del proyecto: {costo_total} unidades.")
    return arbol_resultante


# --- Ejecución de Prueba ---
# Definimos los nodos de nuestra red
nodos_mapa = ['A', 'B', 'C', 'D', 'E', 'Z']
# Definimos todas las conexiones posibles (Origen, Destino, Costo)
# Es el mismo grafo anterior, pero representado como lista de aristas para Kruskal
todas_las_aristas = [
    ('A', 'B', 4), ('A', 'C', 2),
    ('B', 'C', 1), ('B', 'D', 5),
    ('C', 'D', 8), ('C', 'E', 10),
    ('D', 'E', 2), ('D', 'Z', 6),
    ('E', 'Z', 3)
]

# 1. Simular Árbol de Coste Mínimo
print("\n" + "#" * 50)
conexiones_minimas = kruskal_simulador(todas_las_aristas, nodos_mapa, modo="minimo")
time.sleep(3) # Pausa antes de la segunda prueba

# 2. Simular Árbol de Coste Máximo
print("\n" + "#" * 50)
conexiones_maximas = kruskal_simulador(todas_las_aristas, nodos_mapa, modo="maximo")