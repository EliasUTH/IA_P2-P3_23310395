def counting_sort_por_digito(arreglo, exp):
    """
    Función auxiliar para Radix Sort. 
    Ordena el arreglo basándose estrictamente en el dígito representador por 'exp'.
    (exp = 1 para unidades, 10 para decenas, 100 para centenas, etc.)
    """
    n = len(arreglo)
    

    
    # El arreglo de salida que guardará los números ordenados temporalmente
    salida = [0] * n
    


    # Arreglo para contar cuántas veces aparece cada dígito (del 0 al 9)
    conteo = [0] * 10
    


    # 1. Contar cuántos números tienen cada dígito en la posición actual
    for i in range(n):
        # Para extraer el dígito exacto hacemos división entera y módulo 10
        indice_digito = (arreglo[i] // exp) % 10
        conteo[indice_digito] += 1
        


    # 2. Modificar el arreglo 'conteo' para que ahora contenga las posiciones reales
    # que esos dígitos ocuparán en el arreglo de salida.
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]
        


    # 3. Construir el arreglo de salida 
    # (Recorremos el arreglo original de atrás hacia adelante para mantener la estabilidad)
    i = n - 1
    while i >= 0:
        indice_digito = (arreglo[i] // exp) % 10
        salida[conteo[indice_digito] - 1] = arreglo[i]
        conteo[indice_digito] -= 1
        i -= 1



    # 4. Copiar los números ordenados de vuelta al arreglo original
    for i in range(n):
        arreglo[i] = salida[i]



def radix_sort(arreglo):
    """
    Función principal de Radix Sort.
    """
    if not arreglo:
        return []



    # 1. Encontrar el número más grande para saber cuántos dígitos tiene
    # (Si el máximo es 802, sabemos que tiene 3 dígitos, así que daremos 3 pasadas)
    maximo = max(arreglo)



    # 2. Hacer el Counting Sort para cada dígito.
    # 'exp' es el exponente: 1, 10, 100, 1000...
    exp = 1
    while maximo // exp > 0:
        counting_sort_por_digito(arreglo, exp)
        exp *= 10
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = radix_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")