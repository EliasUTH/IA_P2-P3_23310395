def insertion_sort(arreglo):
    """
    Ordena una lista de números utilizando el método de Inserción.
    """
    # En Python, empezamos desde el segundo elemento (índice 1) 
    # porque asumimos que el primer elemento (índice 0) ya es una "lista ordenada" de un solo elemento.
    for i in range(1, len(arreglo)):
        

        
        # 'temp' es la "carta" que tenemos en la mano y queremos insertar
        temp = arreglo[i]
        # 'j' es el índice del elemento inmediatamente anterior a 'temp'
        j = i - 1
        # Mientras no lleguemos al inicio (j >= 0) y el elemento revisado sea MAYOR que 'temp'
        while j >= 0 and arreglo[j] > temp:
            # Movemos el elemento mayor una posición a la derecha
            arreglo[j + 1] = arreglo[j]
            # Seguimos buscando hacia la izquierda
            j -= 1
        # Una vez que encontramos el lugar correcto (donde arreglo[j] ya no es mayor),
        # insertamos 'temp' en el espacio que quedó libre (j + 1)
        arreglo[j + 1] = temp
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [85, 12, 59, 45, 72, 51]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = insertion_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")