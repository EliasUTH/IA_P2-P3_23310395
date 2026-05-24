import math
import random

print("=== ALGORITMO DE RETROPROPAGACIÓN (BACKPROPAGATION) ===\n")

# --- 1. MATEMÁTICAS DE APRENDIZAJE ---
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

def sigmoide_derivada(x):
    # La derivada nos dice hacia dónde y cuánto mover el peso
    return x * (1 - x)

# --- 2. CONFIGURACIÓN DE LA NEURONA ---
# Datos de entrenamiento (XOR simple)
entradas = [0.5, 0.1] 
objetivo = 0.9
tasa_aprendizaje = 0.5

# Pesos iniciales aleatorios
w1, w2 = random.uniform(-1, 1), random.uniform(-1, 1)
peso_salida = random.uniform(-1, 1)
sesgo = random.uniform(-1, 1)

print(f"Pesos iniciales: w1={w1:.2f}, w2={w2:.2f}, ws={peso_salida:.2f}")
print("-" * 50)

# --- 3. CICLO DE APRENDIZAJE (EL CORE) ---
for i in range(1001):
    # --- PASO 1: FORWARD PASS ---
    # (Suma ponderada y activación)
    capa_oculta = sigmoide((entradas[0] * w1) + (entradas[1] * w2) + sesgo)
    prediccion = sigmoide(capa_oculta * peso_salida)

    # --- PASO 2: CÁLCULO DEL ERROR ---
    error = objetivo - prediccion

    # --- PASO 3: BACKPROPAGATION ---
    # A. Calcular el gradiente en la salida
    delta_salida = error * sigmoide_derivada(prediccion)

    # B. Calcular el gradiente en la capa oculta (repartir el error)
    error_oculto = delta_salida * peso_salida
    delta_oculto = error_oculto * sigmoide_derivada(capa_oculta)

    # --- PASO 4: ACTUALIZAR PESOS ---
    peso_salida += tasa_aprendizaje * delta_salida * capa_oculta
    w1 += tasa_aprendizaje * delta_oculto * entradas[0]
    w2 += tasa_aprendizaje * delta_oculto * entradas[1]
    sesgo += tasa_aprendizaje * delta_oculto

    if i % 200 == 0:
        print(f"Iteración {i:4d} | Predicción: {prediccion:.4f} | Error: {error:.4f}")

print("-" * 50)
print(f"Resultado final tras Backpropagation: {prediccion:.4f} (Objetivo: {objetivo})")