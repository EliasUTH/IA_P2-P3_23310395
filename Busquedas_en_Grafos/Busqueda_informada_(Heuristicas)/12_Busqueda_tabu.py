from collections import deque

def tabu_search(f, start, get_neighbors, tabu_size=5, max_iterations=100):
    """
    Implementación básica de la búsqueda tabú (tabu search).

    Parámetros:
    - f: función objetivo a maximizar
    - start: punto de inicio
    - get_neighbors: función que retorna una lista de vecinos para un punto dado
    - tabu_size: tamaño de la lista tabú
    - max_iterations: número máximo de iteraciones

    Retorna:
    - El mejor punto encontrado
    - El valor de la función en ese punto
    """
    current = start
    current_value = f(current)
    best = current
    best_value = current_value
    tabu_list = deque(maxlen=tabu_size)

    for _ in range(max_iterations):
        neighbors = get_neighbors(current)
        # Filtrar vecinos no tabú
        allowed_neighbors = [n for n in neighbors if n not in tabu_list]

        if not allowed_neighbors:
            break  # No hay movimientos permitidos

        # Evaluar vecinos permitidos
        neighbor_values = [(n, f(n)) for n in allowed_neighbors]
        # Elegir el mejor vecino
        next_neighbor, next_value = max(neighbor_values, key=lambda x: x[1])

        # Actualizar mejor si es necesario
        if next_value > best_value:
            best = next_neighbor
            best_value = next_value

        # Moverse al siguiente
        current = next_neighbor
        current_value = next_value

        # Agregar a la lista tabú
        tabu_list.append(current)

    return best, best_value

# Ejemplo de uso
def objective_function(x):
    # Función simple: -x^2 + 10x (máximo en x=5)
    return -x**2 + 10*x

def get_neighbors(x, step_size=1):
    # Vecinos: x-1, x+1
    return [x - step_size, x + step_size]

# Ejecutar tabu search desde x=0
optimal_x, optimal_value = tabu_search(objective_function, start=0, get_neighbors=get_neighbors, tabu_size=3, max_iterations=20)
print(f"Mejor punto encontrado: x = {optimal_x}, valor = {optimal_value}")