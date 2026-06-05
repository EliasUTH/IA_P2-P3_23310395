def merge(arreglo, inicio, medio, fin):
    """
    Función auxiliar para mezclar dos tramos adyacentes.
    (Es la misma lógica que usamos en Straight Merging)
    """
    izquierda = arreglo[inicio:medio]
    derecha = arreglo[medio:fin]  
    i = 0
    j = 0
    k = inicio



    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            arreglo[k] = izquierda[i]
            i += 1
        else:
            arreglo[k] = derecha[j]
            j += 1
        k += 1



    while i < len(izquierda):
        arreglo[k] = izquierda[i]
        i += 1
        k += 1



    while j < len(derecha):
        arreglo[k] = derecha[j]
        j += 1
        k += 1



def natural_merging(arreglo):
    """
    Función principal de Natural Merging.
    Busca "tramos" (secuencias naturales ya ordenadas) y los mezcla.
    """
    n = len(arreglo)
    if n <= 1:
        return arreglo
    ordenado = False



    # Repetimos las pasadas completas hasta que la lista esté totalmente ordenada
    while not ordenado:
        ordenado = True # Asumimos que está ordenado hasta que demostremos lo contrario
        inicio = 0
        while inicio < n:
            # 1. Encontrar el final del PRIMER tramo ordenado natural
            medio = inicio + 1
            while medio < n and arreglo[medio - 1] <= arreglo[medio]:
                medio += 1
            # Si el primer tramo llega hasta el final del arreglo, 
            # no hay un segundo tramo con el cual mezclar en esta iteración.
            if medio == n:
                break
            # 2. Encontrar el final del SEGUNDO tramo ordenado natural
            fin = medio + 1
            while fin < n and arreglo[fin - 1] <= arreglo[fin]:
                fin += 1
            # 3. Mezclar ambos tramos
            merge(arreglo, inicio, medio, fin)            
            # Como tuvimos que hacer una mezcla, significa que la lista global 
            # aún no estaba 100% ordenada desde el principio.
            ordenado = False 
            # Avanzamos al siguiente par de tramos
            inicio = fin           
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista que tiene pequeños "tramos" ya ordenados por accidente
# Tramo 1: [10, 20, 30] | Tramo 2: [5, 15] | Tramo 3: [8, 25, 40]
numeros_desordenados = [10, 20, 30, 5, 15, 8, 25, 40]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = natural_merging(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")