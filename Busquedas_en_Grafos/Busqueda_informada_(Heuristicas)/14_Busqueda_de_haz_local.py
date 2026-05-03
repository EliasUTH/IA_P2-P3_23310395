def local_beam_search(f, initial_states, get_neighbors, beam_width=3, max_iterations=100):
    """
    Implementación básica de la búsqueda de haz local (local beam search).

    Parámetros:
    - f: función objetivo a maximizar
    - initial_states: lista de puntos iniciales
    - get_neighbors: función que retorna una lista de vecinos para un punto dado
    - beam_width: ancho del haz (número de estados a mantener)
    - max_iterations: número máximo de iteraciones

    Retorna:
    - El mejor punto encontrado
    - El valor de la función en ese punto
    """
    # Inicializar el haz con los estados iniciales
    beam = [(state, f(state)) for state in initial_states]
    best = max(beam, key=lambda x: x[1])

    for _ in range(max_iterations):
        # Generar candidatos: todos los vecinos de los estados en el haz
        candidates = []
        for state, _ in beam:
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                candidates.append((neighbor, f(neighbor)))

        if not candidates:
            break

        # Seleccionar los mejores beam_width candidatos
        candidates.sort(key=lambda x: x[1], reverse=True)  # Ordenar por valor descendente
        beam = candidates[:beam_width]

        # Actualizar el mejor global
        current_best = max(beam, key=lambda x: x[1])
        if current_best[1] > best[1]:
            best = current_best

        # Si no hay mejora en el haz, detener (opcional)
        if all(val <= best[1] for _, val in beam):
            break

    return best[0], best[1]

# Ejemplo de uso
def objective_function(x):
    # Función simple: -x^2 + 10x (máximo en x=5)
    return -x**2 + 10*x

def get_neighbors(x, step_size=1):
    # Vecinos: x-1, x+1
    return [x - step_size, x + step_size]

# Ejecutar local beam search con múltiples puntos iniciales
initial_points = [0, 2, 8]  # Empezar desde diferentes puntos
optimal_x, optimal_value = local_beam_search(objective_function, initial_points, get_neighbors, beam_width=3)
print(f"Mejor punto encontrado: x = {optimal_x}, valor = {optimal_value}")