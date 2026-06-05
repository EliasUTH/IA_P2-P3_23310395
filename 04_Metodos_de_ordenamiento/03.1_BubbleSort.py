def bubble_sort(arreglo):
    """
    Ordena una lista de números utilizando el método de Burbuja.
    """
    n = len(arreglo)
    

    
    # El primer bucle asegura que hagamos las pasadas necesarias
    for i in range(n):
        


        # Variable de optimización: si en una pasada no hay intercambios, ya está ordenado
        intercambio = False
        # El segundo bucle compara elementos adyacentes
        # Restamos 'i' al final porque los últimos 'i' elementos ya están ordenados
        for j in range(0, n - i - 1):
            # Si el elemento actual es mayor que el siguiente, se intercambian
            if arreglo[j] > arreglo[j + 1]:
                # En Python, el intercambio se hace en una sola línea (sin variable aux)
                arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]
                intercambio = True
        # Si no hubo ningún intercambio en esta pasada, terminamos antes de tiempo
        if not intercambio:
            break
    return arreglo



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [64, 34, 25, 12, 22, 11, 90]
print(f"Lista original: {numeros_desordenados}")
# 2. Llamamos a la función
numeros_ordenados = bubble_sort(numeros_desordenados.copy()) # Usamos .copy() para no modificar la original
# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")