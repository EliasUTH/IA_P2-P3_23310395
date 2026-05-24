def hill_climbing(f, start, step_size=1, max_iterations=1000):
    """
    Implementación básica de la búsqueda de ascensión de colinas (hill climbing).

    Parámetros:
    - f: función objetivo a maximizar
    - start: punto de inicio
    - step_size: tamaño del paso para generar vecinos
    - max_iterations: número máximo de iteraciones

    Retorna:
    - El punto óptimo encontrado
    - El valor de la función en ese punto
    """
    current = start
    current_value = f(current)

    for _ in range(max_iterations):
        # Generar vecinos
        neighbors = [current - step_size, current + step_size]
        # Evaluar vecinos
        neighbor_values = [(neighbor, f(neighbor)) for neighbor in neighbors]

        # Encontrar el mejor vecino
        best_neighbor, best_value = max(neighbor_values, key=lambda x: x[1])

        # Si el mejor vecino es mejor que el actual, moverse
        if best_value > current_value:
            current = best_neighbor
            current_value = best_value
        else:
            # No hay mejora, detener
            break

    return current, current_value

# Ejemplo de uso
def objective_function(x):
    # Función simple: -x^2 + 10x (máximo en x=5)
    return -x**2 + 10*x

# Ejecutar hill climbing desde x=0
optimal_x, optimal_value = hill_climbing(objective_function, start=0, step_size=1)
print(f"Punto óptimo encontrado: x = {optimal_x}, valor = {optimal_value}")