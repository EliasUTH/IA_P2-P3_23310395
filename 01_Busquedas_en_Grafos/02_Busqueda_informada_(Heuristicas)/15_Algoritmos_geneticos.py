import random

def genetic_algorithm(fitness_func, chromosome_length=5, population_size=10, generations=50, mutation_rate=0.01, crossover_rate=0.7):
    """
    Implementación básica de un algoritmo genético.

    Parámetros:
    - fitness_func: función de aptitud (fitness) a maximizar
    - chromosome_length: longitud del cromosoma (número de bits)
    - population_size: tamaño de la población
    - generations: número de generaciones
    - mutation_rate: probabilidad de mutación por bit
    - crossover_rate: probabilidad de cruce

    Retorna:
    - El mejor cromosoma encontrado
    - Su valor de aptitud
    """

    def create_individual():
        return [random.randint(0, 1) for _ in range(chromosome_length)]

    def decode_chromosome(chromosome):
        # Decodificar binario a entero
        return int(''.join(map(str, chromosome)), 2)

    def fitness(chromosome):
        return fitness_func(decode_chromosome(chromosome))

    def select_parent(population):
        # Selección por torneo
        tournament = random.sample(population, 3)
        return max(tournament, key=fitness)

    def crossover(parent1, parent2):
        if random.random() < crossover_rate:
            point = random.randint(1, chromosome_length - 1)
            return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
        return parent1, parent2

    def mutate(chromosome):
        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    # Inicializar población
    population = [create_individual() for _ in range(population_size)]

    for _ in range(generations):
        # Evaluar aptitud
        population.sort(key=fitness, reverse=True)

        # Crear nueva generación
        new_population = population[:2]  # Elitismo: mantener los 2 mejores

        while len(new_population) < population_size:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(mutate(offspring1))
            if len(new_population) < population_size:
                new_population.append(mutate(offspring2))

        population = new_population

    # Mejor individuo
    best = max(population, key=fitness)
    return best, fitness(best)

# Ejemplo de uso: maximizar x^2 para x en 0-31 (5 bits)
def objective_function(x):
    return x ** 2

random.seed(42)  # Para reproducibilidad
best_chromosome, best_fitness = genetic_algorithm(objective_function, chromosome_length=5, population_size=10, generations=50)
best_x = int(''.join(map(str, best_chromosome)), 2)
print(f"Mejor cromosoma: {best_chromosome} (x = {best_x}), aptitud = {best_fitness}")