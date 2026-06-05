def quick_sort(arreglo):
    """
    Ordena una lista de números utilizando el método QuickSort (Ordenamiento Rápido).
    Utiliza el enfoque 'Divide y Vencerás'.
    """
    # Caso base: Si la lista tiene 1 o 0 elementos, ya está ordenada.
    if len(arreglo) <= 1:
        return arreglo
    

    
    # 1. Elegimos el PIVOTE. 
    # Puede ser cualquier elemento. Aquí elegimos el del medio para mayor eficiencia.
    pivote = arreglo[len(arreglo) // 2]
    # 2. DIVIDIR: Creamos tres sublistas comparando cada elemento con el pivote.
    menores = [x for x in arreglo if x < pivote]
    iguales = [x for x in arreglo if x == pivote]
    mayores = [x for x in arreglo if x > pivote]
    # 3. VENCER (Recursividad) y UNIR: 
    # Ordenamos los menores, ordenamos los mayores y lo pegamos todo junto.
    return quick_sort(menores) + iguales + quick_sort(mayores)



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [33, 10, 59, 27, 41, 10, 8, 95]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
# Nota: Esta versión de QuickSort devuelve una lista nueva, no modifica la original.
numeros_ordenados = quick_sort(numeros_desordenados)



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")