import heapq
def distribucion_tramos_iniciales(arreglo, tamaño_ram, num_cintas):
    """
    Simula la lectura de un archivo grande, la creación de tramos usando
    'Selección por Reemplazo' y su distribución en múltiples cintas.
    """
    if not arreglo:
        return []



    # Simulamos nuestras cintas magnéticas vacías
    cintas = [[] for _ in range(num_cintas)]
    cinta_actual = 0



    # El Heap simulará nuestra memoria RAM limitada
    heap_actual = []



    # Los datos que son menores al último número escrito no pueden ir 
    # en el tramo actual, así que los guardamos en un Heap secundario
    heap_siguiente = []



    # 1. Llenamos la memoria RAM inicial
    idx = 0
    while idx < len(arreglo) and len(heap_actual) < tamaño_ram:
        heapq.heappush(heap_actual, arreglo[idx])
        idx += 1    
    tramo_actual = []
    print(f"--- Iniciando con una RAM de tamaño {tamaño_ram} ---")



    # 2. Procesamos el archivo hasta que nos quedemos sin datos y la RAM esté vacía
    while heap_actual or heap_siguiente or idx < len(arreglo):



        # Si el heap actual se vació, nuestro tramo actual terminó
        if not heap_actual:
            if tramo_actual:
                # Escribimos el tramo en la cinta que toque
                cintas[cinta_actual].append(tramo_actual)
                print(f"Tramo terminado de tamaño {len(tramo_actual)} -> Guardado en Cinta {cinta_actual + 1}")



                # Avanzamos a la siguiente cinta (Distribución Round-Robin simple)
                cinta_actual = (cinta_actual + 1) % num_cintas
                tramo_actual = []



            # Todo lo que no cupo en este tramo se convierte en el inicio del siguiente
            heap_actual = heap_siguiente
            heap_siguiente = []



        # Si hay datos en el heap actual, procesamos
        if heap_actual:
            # Sacamos el menor número de la RAM y lo escribimos en nuestro tramo
            menor = heapq.heappop(heap_actual)
            tramo_actual.append(menor)



            # Si aún hay datos en el archivo gigante, leemos uno nuevo
            if idx < len(arreglo):
                nuevo_valor = arreglo[idx]
                idx += 1
                
 
 
                # MAGIA DE REEMPLAZO:
                # Si el nuevo valor es >= al que acabamos de sacar, puede ir en este mismo tramo
                if nuevo_valor >= menor:
                    heapq.heappush(heap_actual, nuevo_valor)
                # Si es menor, rompería el orden. Lo mandamos al heap del próximo tramo.
                else:
                    heapq.heappush(heap_siguiente, nuevo_valor)



    # 3. Guardar el último tramo si quedó pendiente
    if tramo_actual:
        cintas[cinta_actual].append(tramo_actual)
        print(f"Tramo terminado de tamaño {len(tramo_actual)} -> Guardado en Cinta {cinta_actual + 1}")
    return cintas



# --- Prueba del algoritmo ---
# Simulamos un archivo de datos desordenados
archivo_gigante = [51, 24, 15, 87, 43, 90, 62, 10, 33, 76, 5, 88, 12, 45, 99, 1]



# Llamamos a la función:
# Vamos a decir que nuestra RAM solo puede guardar 3 números a la vez, 
# y queremos distribuir los tramos en 2 cintas magnéticas.
cintas_resultantes = distribucion_tramos_iniciales(archivo_gigante, tamaño_ram=3, num_cintas=2)



print("\n--- RESULTADO DE LA DISTRIBUCIÓN ---")
for i, cinta in enumerate(cintas_resultantes):
    print(f"Cinta {i + 1} contiene los tramos: {cinta}")