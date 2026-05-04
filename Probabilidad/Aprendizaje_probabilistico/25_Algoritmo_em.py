import random
import math

print("=== ALGORITMO EM (EXPECTATION-MAXIMIZATION) ===\n")

# --- 1. PREPARACIÓN DE DATOS (Mundo Real) ---
# Creamos dos grupos de datos reales que la IA intentará separar
grupo_A = [random.gauss(10, 2) for _ in range(50)]  # Media real: 10
grupo_B = [random.gauss(40, 5) for _ in range(50)]  # Media real: 40
datos = grupo_A + grupo_B
random.shuffle(datos)

def pdf_gaussiana(x, media, desviacion):
    """Función de densidad de probabilidad Gaussiana"""
    exponente = math.exp(-((x - media) ** 2) / (2 * (desviacion ** 2)))
    return (1 / (math.sqrt(2 * math.pi) * desviacion)) * exponente

# --- 2. EL ALGORITMO EM ---

# Inicialización ciega (la IA empieza adivinando)
m1, d1 = 5.0, 2.0   # Parámetros grupo 1
m2, d2 = 50.0, 2.0  # Parámetros grupo 2

iteraciones = 20
print(f"{'Iteración':<10} | {'Media 1 (Est.)':<15} | {'Media 2 (Est.)'}")
print("-" * 45)

for i in range(iteraciones):
    # --- PASO E: Esperanza ---
    # Calculamos la probabilidad de cada dato de pertenecer a m1 o m2
    responsabilidades = []
    for x in datos:
        prob1 = pdf_gaussiana(x, m1, d1)
        prob2 = pdf_gaussiana(x, m2, d2)
        total = prob1 + prob2
        responsabilidades.append(prob1 / total)

    # --- PASO M: Maximización ---
    # Usamos las 'pesos' (responsabilidades) para calcular nuevas medias
    sum_resp1 = sum(responsabilidades)
    sum_resp2 = len(datos) - sum_resp1
    
    m1 = sum(r * x for r, x in zip(responsabilidades, datos)) / sum_resp1
    m2 = sum((1 - r) * x for r, x in zip(responsabilidades, datos)) / sum_resp2
    
    # (Para simplificar, mantenemos la desviación fija, pero EM también podría ajustarla)

    if i % 2 == 0 or i == iteraciones - 1:
        print(f"{i+1:<10} | {m1:<15.4f} | {m2:.4f}")

print("\n=== RESULTADO FINAL ===")
print(f"La IA encontró los centros en: {m1:.2f} y {m2:.2f}")
print("¡Muy cerca de los originales (10 y 40)!")