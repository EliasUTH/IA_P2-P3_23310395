def merge(izquierda, derecha):
    """
    Función auxiliar que toma dos listas ya ordenadas 
    y las fusiona (mezcla) en una sola lista ordenada.
    """
    resultado = []
    i = 0 # Índice para recorrer la lista izquierda
    j = 0 # Índice para recorrer la lista derecha
    

    
    # Comparamos los elementos de ambas listas y agregamos el menor al resultado
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1



    # Si sobraron elementos en alguna de las listas (porque la otra ya se vació),
    # simplemente los agregamos al final del resultado
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado



def merge_sort(arreglo):
    """
    Función principal de Ordenamiento por Mezcla.
    Divide recursivamente la lista a la mitad y luego las fusiona.
    """
    # Caso base: Si la lista tiene 1 o 0 elementos, ya está ordenada
    if len(arreglo) <= 1:
        return arreglo
    # 1. DIVIDIR: Encontramos la mitad de la lista
    medio = len(arreglo) // 2
    # Partimos la lista en dos mitades
    mitad_izquierda = arreglo[:medio]
    mitad_derecha = arreglo[medio:]
    # 2. VENCER (Recursividad): Ordenamos cada mitad de forma independiente
    mitad_izquierda_ordenada = merge_sort(mitad_izquierda)
    mitad_derecha_ordenada = merge_sort(mitad_derecha)
    # 3. UNIR: Mezclamos las dos mitades ya ordenadas
    return merge(mitad_izquierda_ordenada, mitad_derecha_ordenada)



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [38, 27, 43, 3, 9, 82, 10]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = merge_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")