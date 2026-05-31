def selection_sort(arreglo):
    """
    Ordena una lista de números utilizando el método de Selección.
    Busca el elemento más pequeño y lo coloca al principio.
    """
    n = len(arreglo)
    

    
    # Recorremos toda la lista
    for i in range(n):
        # Suponemos que el primer elemento no ordenado es el más pequeño
        indice_minimo = i
        # Buscamos en el resto de la lista (de i+1 hasta el final) si hay uno aún más pequeño
        for j in range(i + 1, n):
            if arreglo[j] < arreglo[indice_minimo]:
                # Si encontramos uno menor, actualizamos la posición del mínimo
                indice_minimo = j    
        # Una vez que encontramos el número más pequeño real en la parte restante,
        # lo intercambiamos con el primer elemento no ordenado (el de la posición 'i')
        # (Nuevamente, aprovechamos el intercambio en una sola línea de Python)
        arreglo[i], arreglo[indice_minimo] = arreglo[indice_minimo], arreglo[i]     
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [64, 25, 12, 22, 11]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = selection_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")