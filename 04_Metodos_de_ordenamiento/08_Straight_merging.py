def merge_directo(arreglo, inicio, medio, fin):
    """
    Función auxiliar que mezcla dos porciones adyacentes de un arreglo.
    Porción izquierda: desde 'inicio' hasta 'medio'
    Porción derecha: desde 'medio' hasta 'fin'
    """
    # Extraemos las dos sublistas a mezclar
    izquierda = arreglo[inicio:medio]
    derecha = arreglo[medio:fin]
    

    
    i = 0  # Índice para la sublista izquierda
    j = 0  # Índice para la sublista derecha
    k = inicio  # Índice para reescribir en el arreglo original
    


    # Comparamos y colocamos el menor de vuelta en el arreglo original
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            arreglo[k] = izquierda[i]
            i += 1
        else:
            arreglo[k] = derecha[j]
            j += 1
        k += 1
        


    # Si sobraron elementos en la izquierda, los copiamos
    while i < len(izquierda):
        arreglo[k] = izquierda[i]
        i += 1
        k += 1
        


    # Si sobraron elementos en la derecha, los copiamos
    while j < len(derecha):
        arreglo[k] = derecha[j]
        j += 1
        k += 1



def straight_merging(arreglo):
    """
    Función principal de Straight Merging (Bottom-Up Merge Sort).
    Ordena la lista de forma iterativa, sin usar recursividad.
    """
    n = len(arreglo)
    tamaño_sublista = 1
    


    # El tamaño de las sublistas se va duplicando: 1, 2, 4, 8, 16...
    while tamaño_sublista < n:
        izq = 0       
        # Recorremos el arreglo de izquierda a derecha saltando en bloques
        while izq < n:
            # Calculamos dónde termina la primera sublista (y empieza la segunda)
            medio = min(izq + tamaño_sublista, n)           
            # Calculamos dónde termina la segunda sublista
            der = min(izq + 2 * tamaño_sublista, n)          
            # Mezclamos ambas sublistas
            merge_directo(arreglo, izq, medio, der)           
            # Avanzamos al siguiente par de sublistas
            izq += 2 * tamaño_sublista
        # Duplicamos el tamaño para la siguiente pasada general
        tamaño_sublista *= 2
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [65, 12, 89, 43, 21, 5, 78, 34, 99]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = straight_merging(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")