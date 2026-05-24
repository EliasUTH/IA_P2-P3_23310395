import random
import math

print("=== AGRUPAMIENTO NO SUPERVISADO (K-MEANS) ===\n")

# --- 1. GENERACIÓN DE DATOS (Sin etiquetas) ---
# Creamos tres grupos de puntos en un espacio 1D para que la IA los encuentre
datos = (
    [random.uniform(0, 10) for _ in range(20)] +   # Grupo Bajo
    [random.uniform(40, 50) for _ in range(20)] +  # Grupo Medio
    [random.uniform(80, 90) for _ in range(20)]    # Grupo Alto
)
random.shuffle(datos)

# --- 2. EL ALGORITMO K-MEANS ---

def calcular_distancia(p1, p2):
    return abs(p1 - p2)

def k_means(dataset, k, iteraciones=10):
    # Paso 1: Inicialización - Elegimos k puntos al azar como centros iniciales
    centroides = random.sample(dataset, k)
    
    for i in range(iteraciones):
        # Paso 2: Asignación - Cada punto se va al grupo del centroide más cercano
        grupos = [[] for _ in range(k)]
        for punto in dataset:
            distancias = [calcular_distancia(punto, c) for c in centroides]
            indice_cercano = distancias.index(min(distancias))
            grupos[indice_cercano].append(punto)
        
        # Paso 3: Actualización - El centroide se mueve al promedio de su grupo
        nuevos_centroides = []
        for g in grupos:
            if g: # Evitar división por cero si un grupo queda vacío
                nuevos_centroides.append(sum(g) / len(g))
            else:
                nuevos_centroides.append(random.choice(dataset))
        
        centroides = nuevos_centroides
        print(f"Iteración {i+1}: Centros en {[round(c, 2) for c in centroides]}")

    return centroides, grupos

# --- 3. EJECUCIÓN ---

K = 3 # Queremos encontrar los 3 grupos que creamos arriba
centros_finales, grupos_finales = k_means(datos, K)

print("\n=== RESULTADO DEL AGRUPAMIENTO ===")
for i, centro in enumerate(centros_finales):
    print(f"Grupo {i+1}: Centroide en {centro:.2f} (Contiene {len(grupos_finales[i])} puntos)")

print("\n=== PERSPECTIVA DE LA IA ===")
print("La IA no sabía que los datos venían de rangos 0-10, 40-50 y 80-90.")
print("Al iterar entre 'asignar puntos' y 'mover centros', el algoritmo")
print("minimizó la varianza interna y descubrió la estructura del mundo por sí solo.")