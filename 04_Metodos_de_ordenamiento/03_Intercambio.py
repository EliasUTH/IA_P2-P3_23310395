def exchange_sort(arreglo):
    """
    Ordena una lista de números utilizando el método de Intercambio.
    Compara el elemento actual con todos los siguientes y los intercambia
    inmediatamente si están desordenados.
    """
    n = len(arreglo)


    
    
    # Recorremos la lista hasta el penúltimo elemento
    for i in range(n - 1): 
        # Comparamos el elemento 'i' con todos los elementos que le siguen
        for j in range(i + 1, n):
            # Si el elemento en la posición 'i' es mayor que el evaluado en 'j'
            if arreglo[i] > arreglo[j]:
                # ¡Intercambio inmediato!
                arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [50, 20, 40, 10, 30]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = exchange_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")