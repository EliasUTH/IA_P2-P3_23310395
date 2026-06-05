# 1. Definimos la estructura de una "hoja" o "nodo" del árbol
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None # Rama para números menores
        self.derecha = None   # Rama para números mayores



# 2. Función para ir construyendo el árbol
def insertar(raiz, valor):
    """
    Inserta un nuevo valor en el Árbol Binario de Búsqueda.
    """
    # Si el árbol está vacío, este valor se convierte en la raíz
    if raiz is None:
        return Nodo(valor)  
    # Si el valor es menor, se va por la rama izquierda
    if valor < raiz.valor:
        raiz.izquierda = insertar(raiz.izquierda, valor)
    # Si el valor es mayor o igual, se va por la rama derecha
    else:
        raiz.derecha = insertar(raiz.derecha, valor)    
    return raiz



# 3. Función para extraer los números ordenados
def recorrido_inorden(raiz, lista_ordenada):
    """
    Recorre el árbol en orden: Izquierda -> Centro -> Derecha
    """
    if raiz is not None:
        # Primero vamos a lo más profundo de la izquierda (los más pequeños)
        recorrido_inorden(raiz.izquierda, lista_ordenada) 
        # Luego guardamos el valor actual
        lista_ordenada.append(raiz.valor)  
        # Finalmente vamos a la derecha (los más grandes)
        recorrido_inorden(raiz.derecha, lista_ordenada)



# 4. Función principal que une todo el proceso
def tree_sort(arreglo):
    """
    Ordena una lista utilizando el método de Ordenamiento de Árbol.
    """
    if not arreglo:
        return []
    # Paso 1: Construir el árbol con el primer elemento como raíz
    raiz = Nodo(arreglo[0])
    for i in range(1, len(arreglo)):
        insertar(raiz, arreglo[i])
    # Paso 2: Leer el árbol construido para obtener la lista ordenada
    resultado = []
    recorrido_inorden(raiz, resultado)
    return resultado



# --- Prueba del algoritmo ---
# 1. Definimos una lista desordenada
numeros_desordenados = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(f"Lista original: {numeros_desordenados}")



# 2. Llamamos a la función
numeros_ordenados = tree_sort(numeros_desordenados.copy())



# 3. Mostramos el resultado
print(f"Lista ordenada: {numeros_ordenados}")