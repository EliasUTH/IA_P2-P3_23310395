import numpy as np
import random

# 1. Configuración del Casino (Entorno)
# Tres máquinas tragamonedas. Sus probabilidades reales de ganar (el agente NO las conoce)
probabilidades_reales = [0.2, 0.7, 0.4] # La máquina 1 es la mejor (70% de ganar)
n_maquinas = len(probabilidades_reales)

# 2. Configuración del Agente de IA
# epsilon = 0.1 significa: 10% del tiempo explora, 90% del tiempo explota
epsilon = 0.1 
intentos_totales = 1000

# Memoria del agente: Cuántas veces ha jugado en cada máquina y cuál es el premio promedio
veces_jugadas = np.zeros(n_maquinas)
recompensa_estimada = np.zeros(n_maquinas)

# 3. Bucle de Simulación
recompensa_total = 0

for intento in range(intentos_totales):
    # --- LA DECISIÓN CRÍTICA: ¿Explorar o Explotar? ---
    probabilidad_aleatoria = random.uniform(0, 1)
    
    if probabilidad_aleatoria < epsilon:
        # EXPLORACIÓN: Elegir una máquina completamente al azar
        accion = random.randint(0, n_maquinas - 1)
        tipo_accion = "Exploró"
    else:
        # EXPLOTACIÓN: Elegir la máquina que tiene el mejor promedio de ganancias hasta ahora
        accion = np.argmax(recompensa_estimada)
        tipo_accion = "Explotó"
        
    # --- JUGAR EN LA MÁQUINA ELEGIDA ---
    # Simulamos si gana (1) o pierde (0) basándonos en la probabilidad real de la máquina
    if random.uniform(0, 1) < probabilidades_reales[accion]:
        recompensa = 1
    else:
        recompensa = 0
        
    recompensa_total += recompensa
    
    # --- ACTUALIZAR LA MEMORIA DEL AGENTE ---
    veces_jugadas[accion] += 1
    
    # Fórmula para actualizar el promedio: 
    # Nuevo Promedio = Promedio Anterior + (1/veces_jugadas) * (Recompensa - Promedio Anterior)
    n = veces_jugadas[accion]
    valor_antiguo = recompensa_estimada[accion]
    
    recompensa_estimada[accion] = valor_antiguo + (1/n) * (recompensa - valor_antiguo)

# 4. Resultados Finales
print("=== RESULTADOS DEL APRENDIZAJE ===")
print(f"Estrategia Epsilon: {epsilon} ({epsilon*100}% Exploración)")
print(f"Recompensa total ganada: {recompensa_total} de {intentos_totales} intentos\n")

for i in range(n_maquinas):
    print(f"Máquina {i}:")
    print(f" - Probabilidad Real (Oculta): {probabilidades_reales[i] * 100}%")
    print(f" - Lo que la IA estimó:      {round(recompensa_estimada[i] * 100, 2)}%")
    print(f" - Veces que decidió jugarla: {int(veces_jugadas[i])} veces\n")