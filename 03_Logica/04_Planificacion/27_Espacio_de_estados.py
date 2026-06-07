from collections import deque
class ProblemaJarras:
    """
    Define la estructura del Espacio de Estados para el problema de las jarras.
    Cada 'estado' se representa como una tupla (litros_en_A, litros_en_B).
    """
    def __init__(self):
        self.capacidad_a = 4
        self.capacidad_b = 3
        self.estado_inicial = (0, 0) # Ambas jarras empiezan vacias
        self.meta = 2 # Queremos exactamente 2 litros en la Jarra A



    def es_meta(self, estado):
        """Prueba de meta: Verifica si hemos llegado al estado deseado."""
        return estado[0] == self.meta



    def obtener_transiciones(self, estado):
        """
        Dado un estado actual, calcula todos los estados adyacentes posibles.
        Esta funcion es el 'motor' que genera el Espacio de Estados dinamicamente.
        """
        sucesores = []
        a, b = estado


        # Accion 1: Llenar la Jarra A desde la fuente
        if a < self.capacidad_a:
            sucesores.append(((self.capacidad_a, b), "Llenar Jarra A"))
            

        # Accion 2: Llenar la Jarra B desde la fuente
        if b < self.capacidad_b:
            sucesores.append(((a, self.capacidad_b), "Llenar Jarra B"))


        # Accion 3: Vaciar la Jarra A en el suelo
        if a > 0:
            sucesores.append(((0, b), "Vaciar Jarra A"))


        # Accion 4: Vaciar la Jarra B en el suelo
        if b > 0:
            sucesores.append(((a, 0), "Vaciar Jarra B"))
            

        # Accion 5: Verter agua de A hacia B hasta que B se llene o A se vacie
        if a > 0 and b < self.capacidad_b:
            # Calculamos cuanta agua realmente puede transferirse
            cantidad = min(a, self.capacidad_b - b)
            sucesores.append(((a - cantidad, b + cantidad), "Verter de A hacia B"))
            

        # Accion 6: Verter agua de B hacia A hasta que A se llene o B se vacie
        if b > 0 and a < self.capacidad_a:
            cantidad = min(b, self.capacidad_a - a)
            sucesores.append(((a + cantidad, b - cantidad), "Verter de B hacia A"))
        return sucesores



def exploracion_espacio_estados(problema):
    """
    Navega por el espacio de estados usando Busqueda en Amplitud (BFS)
    para garantizar que se encuentre la secuencia de acciones mas corta.
    """
    print("Iniciando exploracion del Espacio de Estados...")
    


    # La cola guarda rutas completas. Una ruta es una lista de tuplas (estado, accion_tomada)
    # Iniciamos la cola con la ruta que contiene solo el estado inicial
    ruta_inicial = [(problema.estado_inicial, "Inicio")]
    cola = deque([ruta_inicial])
    


    # Conjunto para recordar que nodos (estados) ya evaluamos y evitar bucles infinitos
    estados_visitados = set()
    estados_visitados.add(problema.estado_inicial)
    nodos_explorados = 0



    while cola:
        # Extraemos la ruta mas antigua de la cola
        ruta_actual = cola.popleft()
        # El estado actual es el ultimo estado de la ruta
        estado_actual, _ = ruta_actual[-1]
        nodos_explorados += 1


        # 1. Verificamos si este estado resuelve el problema
        if problema.es_meta(estado_actual):
            print(f"Meta alcanzada tras explorar {nodos_explorados} nodos (estados posibles).")
            return ruta_actual


        # 2. Si no es la meta, generamos sus sucesores y expandimos el arbol
        for estado_siguiente, accion in problema.obtener_transiciones(estado_actual):
            if estado_siguiente not in estados_visitados:
                estados_visitados.add(estado_siguiente)
                

                # Creamos una nueva ruta copiando la actual y añadiendo el nuevo paso
                nueva_ruta = list(ruta_actual)
                nueva_ruta.append((estado_siguiente, accion))
                cola.append(nueva_ruta)

    print("Se agoto el espacio de estados sin encontrar solucion.")
    return None



# EJECUCION DEL ALGORITMO
if __name__ == "__main__":
    problema_jarras = ProblemaJarras()
    solucion = exploracion_espacio_estados(problema_jarras)
    
    if solucion:
        print("\n___Secuencia optima de acciones encontrada___")
        paso_num = 0
        for estado, accion in solucion:
            if paso_num == 0:
                print(f"Estado Inicial: Jarra A = {estado[0]}L, Jarra B = {estado[1]}L")
            else:
                print(f"Paso {paso_num}: {accion}")
                print(f"         -> Nuevo estado: Jarra A = {estado[0]}L, Jarra B = {estado[1]}L")
            paso_num += 1