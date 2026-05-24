import random

print("=== MCMC: MONTE CARLO POR CADENAS DE MARKOV ===\n")

# 1. Definir la MATRIZ DE TRANSICIÓN (La Cadena de Markov)
# Regla: La probabilidad del clima de mañana SOLO depende del clima de hoy.
# Las sumas de cada fila deben dar 1.0 (100%)

estados = ["Soleado", "Nublado", "Lluvia"]

# Diccionario de transiciones: Estado Actual -> {Probabilidades del Estado Siguiente}
matriz_transicion = {
    "Soleado": {"Soleado": 0.70, "Nublado": 0.20, "Lluvia": 0.10},
    "Nublado": {"Soleado": 0.30, "Nublado": 0.40, "Lluvia": 0.30},
    "Lluvia":  {"Soleado": 0.20, "Nublado": 0.30, "Lluvia": 0.50}
}

# 2. Motor MCMC (El "Caminante Aleatorio")
def simular_mcmc(estado_inicial, pasos):
    """
    Simula una caminata aleatoria a través de la cadena de Markov.
    """
    estado_actual = estado_inicial
    conteo_estados = {"Soleado": 0, "Nublado": 0, "Lluvia": 0}
    
    # El algoritmo da miles de 'pasos' en el tiempo
    for _ in range(pasos):
        # Registramos dónde estamos hoy
        conteo_estados[estado_actual] += 1
        
        # Miramos las reglas (probabilidades) de a dónde podemos ir mañana
        opciones_futuras = list(matriz_transicion[estado_actual].keys())
        probabilidades_futuras = list(matriz_transicion[estado_actual].values())
        
        # Damos el salto al mañana usando la ruleta de Monte Carlo
        # (random.choices devuelve una lista, extraemos el primer elemento [0])
        estado_actual = random.choices(opciones_futuras, weights=probabilidades_futuras)[0]
        
    # Calculamos el porcentaje de tiempo que pasamos en cada estado (Distribución Estacionaria)
    distribucion_final = {estado: (conteo / pasos) for estado, conteo in conteo_estados.items()}
    
    return distribucion_final

# --- SIMULACIÓN DE LA IA ---

dias_a_simular = 50000
clima_hoy = "Lluvia"

print(f"Estado Inicial (Hoy): {clima_hoy}")
print(f"Simulando el clima para los próximos {dias_a_simular} días usando MCMC...\n")

# Ejecutamos el algoritmo
distribucion_estacionaria = simular_mcmc(clima_hoy, dias_a_simular)

print("=== DISTRIBUCIÓN ESTACIONARIA (A LARGO PLAZO) ===")
for clima, prob in distribucion_estacionaria.items():
    print(f"-> Probabilidad de {clima:<8}: {prob * 100:.2f}%")

print("\n=== VEREDICTO DE LA INTELIGENCIA ARTIFICIAL ===")
print("La IA no resolvió ni una sola ecuación de álgebra lineal.")
print("Simplemente dejó a un 'agente virtual' saltar de un clima a otro 50,000 veces")
print("siguiendo las reglas de Markov. Al final, simplemente contó los días.")
print("\nConclusión: No importa si hoy es un día de 'Lluvia' o 'Soleado',")
print("a largo plazo, esta ciudad pasará aproximadamente el 47% de su existencia")
print("soleada, el 28% nublada y el 25% lloviendo.")