import heapq
def multiway_merge_sort(arreglo, k=3):
    """
    Ordenamiento por Mezcla Equilibrada de Múltiples Vías (k-way Merge Sort).
    Divide la lista en 'k' partes, las ordena recursivamente y las mezcla de golpe.
    """
    n = len(arreglo)



    # Caso base: si la lista tiene 1 o 0 elementos, ya está ordenada.
    if n <= 1:
        return arreglo



    # Si pedimos dividir en más vías que elementos disponibles, ajustamos 'k'
    k = min(k, n)



    # 1. DIVIDIR el arreglo en 'k' sublistas de tamaño similar
    # Calculamos el tamaño aproximado de cada bloque
    tamaño_bloque = (n + k - 1) // k  
    sublistas = []



    for i in range(k):
        inicio = i * tamaño_bloque
        fin = min(inicio + tamaño_bloque, n)
        if inicio < n:
            sublistas.append(arreglo[inicio:fin])



    # 2. VENCER (Recursividad): Ordenamos recursivamente cada una de las 'k' sublistas
    sublistas_ordenadas = [multiway_merge_sort(sub, k) for sub in sublistas]



    # 3. UNIR (Multiway Merge): 
    # Aquí está la magia. En lugar de mezclar de 2 en 2, usamos heapq.merge 
    # que toma múltiples listas ordenadas y extrae el menor de TODAS ellas al mismo tiempo.
    # El asterisco (*) desempaqueta la lista de listas para que la función las lea individualmente.
    resultado = list(heapq.merge(*sublistas_ordenadas))   
    return resultado



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [88, 14, 53, 91, 25, 7, 62, 39, 10, 45, 71, 3]
print(f"Lista original ({len(numeros_desordenados)} elementos): {numeros_desordenados}")



# 2. Llamamos a la función indicando que use un sistema de 3 vías (k=3)
numeros_ordenados = multiway_merge_sort(numeros_desordenados.copy(), k=3)



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")