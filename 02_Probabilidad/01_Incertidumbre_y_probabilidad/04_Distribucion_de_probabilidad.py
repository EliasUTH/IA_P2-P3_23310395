import random

print("=== DISTRIBUCIÓN DE PROBABILIDAD EN IA ===\n")

# Escenario: Una IA ha analizado una foto borrosa y genera una 
# Distribución de Probabilidad sobre lo que cree que hay en la imagen.
# Regla de oro: La suma de todas las probabilidades DEBE ser exactamente 1.0 (100%)

distribucion_clases = {
    "Gato": 0.70,     # 70% de probabilidad
    "Perro": 0.20,    # 20% de probabilidad
    "Pájaro": 0.08,   # 8% de probabilidad
    "Ruido": 0.02     # 2% de probabilidad (no sabe qué es)
}

# Verificamos que sea una distribución válida
suma_probabilidades = sum(distribucion_clases.values())
print(f"Suma total de la distribución: {suma_probabilidades * 100}%\n")

# Separar las clases y sus probabilidades para usarlas en la simulación
clases = list(distribucion_clases.keys())
probabilidades = list(distribucion_clases.values())

print("Si la IA tuviera que adivinar 1 sola vez, tomaría la de mayor probabilidad (Gato).")
print("Pero, ¿qué pasa si simulamos esta distribución 10,000 veces usando el azar ponderado?\n")

# 1. Realizar una Simulación de Monte Carlo (muestreo de la distribución)
simulaciones = 10000
resultados_obtenidos = {"Gato": 0, "Perro": 0, "Pájaro": 0, "Ruido": 0}

# random.choices toma elementos basándose en una lista de probabilidades (weights)
# Es como tirar un dado cargado
muestras = random.choices(clases, weights=probabilidades, k=simulaciones)

# 2. Contar los resultados de la simulación
for resultado in muestras:
    resultados_obtenidos[resultado] += 1

# 3. Mostrar los resultados comparando la teoría vs la práctica
print(f"--- RESULTADOS TRAS {simulaciones} SIMULACIONES ---")
print("Clase   | Prob. Teórica | Resultados Prácticos | Frecuencia Simulada")
print("-" * 65)

for clase in clases:
    prob_teorica = distribucion_clases[clase] * 100
    cantidad_practica = resultados_obtenidos[clase]
    frecuencia_simulada = (cantidad_practica / simulaciones) * 100
    
    # Formateo para que se vea como una tabla bonita en la terminal
    print(f"{clase:<7} | {prob_teorica:>6.1f}%      | {cantidad_practica:>18} | {frecuencia_simulada:>18.2f}%")

print("\nConclusión de la IA:")
print("A medida que el número de simulaciones crece, la 'Frecuencia Simulada'")
print("se acerca casi perfectamente a la 'Probabilidad Teórica'. Esto se conoce como")
print("la Ley de los Grandes Números.")