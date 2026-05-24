import math
import random

def simulated_annealing(f, start, get_neighbors, initial_temp=100, cooling_rate=0.95, min_temp=1e-3, max_iterations=1000):
    """
    Implementación básica de la búsqueda de temple simulado (simulated annealing).

    Parámetros:
    - f: función objetivo a maximizar
    - start: punto de inicio
    - get_neighbors: función que retorna una lista de vecinos para un punto dado
    - initial_temp: temperatura inicial
    - cooling_rate: factor de enfriamiento (0 < cooling_rate < 1)
    - min_temp: temperatura mínima para detener
    - max_iterations: número máximo de iteraciones

    Retorna:
    - El mejor punto encontrado
    - El valor de la función en ese punto
    """
    current = start
    current_value = f(current)
    best = current
    best_value = current_value
    temp = initial_temp

    for _ in range(max_iterations):
        if temp < min_temp:
            break

        neighbors = get_neighbors(current)
        if not neighbors:
            break

        # Elegir un vecino aleatorio
        next_candidate = random.choice(neighbors)
        next_value = f(next_candidate)

        # Calcular delta (diferencia de energía)
        delta = next_value - current_value

        # Aceptar si es mejor o con probabilidad exp(-delta/temp)
        if delta > 0 or random.random() < math.exp(delta / temp):
            current = next_candidate
            current_value = next_value

            # Actualizar mejor si es necesario
            if current_value > best_value:
                best = current
                best_value = current_value

        # Enfriar temperatura
        temp *= cooling_rate

    return best, best_value

# Ejemplo de uso
def objective_function(x):
    # Función simple: -x^2 + 10x (máximo en x=5)
    return -x**2 + 10*x

def get_neighbors(x, step_size=1):
    # Vecinos: x-1, x+1
    return [x - step_size, x + step_size]

# Ejecutar simulated annealing desde x=0
random.seed(42)  # Para reproducibilidad
optimal_x, optimal_value = simulated_annealing(objective_function, start=0, get_neighbors=get_neighbors)
print(f"Mejor punto encontrado: x = {optimal_x}, valor = {optimal_value}")