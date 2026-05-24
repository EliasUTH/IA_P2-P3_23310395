import math
import random

print("=== MAPA AUTOORGANIZADO DE KOHONEN (SOM) ===\n")

# --- 1. CONFIGURACIÓN DEL MAPA ---
# Vamos a organizar colores (RGB: 3 dimensiones) en una rejilla 1D para simplificar
FILAS = 1
COLUMNAS = 10
DIM_ENTRADA = 3 # Red, Green, Blue
TASA_APRENDIZAJE_INICIAL = 0.5
RADIO_INICIAL = COLUMNAS / 2

# Creamos la rejilla de neuronas con pesos aleatorios
# Cada neurona tiene 3 pesos (uno por cada color R, G, B)
mapa = [[random.random() for _ in range(DIM_ENTRADA)] for _ in range(COLUMNAS)]

# --- 2. DATOS DE ENTRENAMIENTO (Colores puros) ---
colores = [
    [1, 0, 0], # Rojo
    [0, 1, 0], # Verde
    [0, 0, 1], # Azul
    [1, 1, 0], # Amarillo
    [0, 1, 1]  # Cian
]

def distancia_euclidiana(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

# --- 3. ENTRENAMIENTO ---
epocas = 500
for t in range(epocas):
    # Seleccionar un color al azar
    target = random.choice(colores)
    
    # PASO A: Encontrar la BMU (Best Matching Unit) - La neurona más parecida
    bmu_idx = 0
    dist_min = distancia_euclidiana(target, mapa[0])
    
    for i in range(1, COLUMNAS):
        dist = distancia_euclidiana(target, mapa[i])
        if dist < dist_min:
            dist_min = dist
            bmu_idx = i
            
    # PASO B: Actualizar la BMU y sus vecinas
    # El radio y la tasa de aprendizaje decaen con el tiempo
    radio_actual = RADIO_INICIAL * math.exp(-t / epocas)
    tasa_actual = TASA_APRENDIZAJE_INICIAL * math.exp(-t / epocas)
    
    for i in range(COLUMNAS):
        dist_nodos = abs(i - bmu_idx) # Distancia en la rejilla
        
        if dist_nodos <= radio_actual:
            # Influencia basada en la distancia (Campana de Gauss)
            influencia = math.exp(-(dist_nodos**2) / (2 * (radio_actual**2)))
            
            # Ajustar pesos de la neurona
            for j in range(DIM_ENTRADA):
                mapa[i][j] += tasa_actual * influencia * (target[j] - mapa[i][j])

# --- 4. RESULTADO ---
print("Mapa final (Representación de colores aprendidos):")
print("-" * 60)
for i, neurona in enumerate(mapa):
    r, g, b = [round(c, 2) for c in neurona]
    print(f"Neurona {i}: R:{r:<4} G:{g:<4} B:{b:<4} | Intensidad Dominante: {['R','G','B'][neurona.index(max(neurona))]}")

print("\n=== ANÁLISIS DEL EXPERTO ===")
print("1. Nota cómo neuronas contiguas tienen colores parecidos.")
print("2. La red ha 'proyectado' colores 3D en una línea 1D manteniendo la vecindad.")
print("3. Este es un aprendizaje competitivo: las neuronas compiten por ser la BMU.")