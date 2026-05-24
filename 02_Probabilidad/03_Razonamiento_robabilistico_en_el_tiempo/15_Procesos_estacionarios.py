import random

print("=== PROCESOS ESTOCÁSTICOS EN EL TIEMPO ===\n")

def generar_ruido():
    """Genera una perturbación aleatoria (ruido blanco) entre -1 y 1"""
    return random.uniform(-1, 1)

def calcular_media(lista):
    return sum(lista) / len(lista)

# --- 1. PROCESO ESTACIONARIO (Autorregresivo AR(1) con p < 1) ---
# La fórmula es: X_t = (0.5 * X_t-1) + ruido
# Al multiplicar por 0.5, "jalamos" el valor siempre de regreso hacia el cero (Reversión a la media).
def simular_estacionario(pasos):
    valores = [0.0]  # Iniciamos en 0
    for _ in range(pasos):
        # El pasado importa, pero pierde fuerza (0.5), y le sumamos un evento aleatorio
        nuevo_valor = (0.5 * valores[-1]) + generar_ruido()
        valores.append(nuevo_valor)
    return valores

# --- 2. PROCESO NO ESTACIONARIO (Caminata Aleatoria / Random Walk) ---
# La fórmula es: Y_t = Y_t-1 + ruido
# Todo el pasado se acumula intacto. La varianza explota hacia el infinito.
def simular_no_estacionario(pasos):
    valores = [0.0]  # Iniciamos en 0
    for _ in range(pasos):
        # Todo el valor pasado se transfiere completo (1.0), más el ruido
        nuevo_valor = valores[-1] + generar_ruido()
        valores.append(nuevo_valor)
    return valores

# --- EJECUCIÓN Y ANÁLISIS ---

dias_simulados = 3000

print(f"Simulando ambos procesos por {dias_simulados} pasos de tiempo...\n")

serie_estacionaria = simular_estacionario(dias_simulados)
serie_no_estacionaria = simular_no_estacionario(dias_simulados)

# Vamos a dividir la historia en 3 épocas (Inicio, Mitad, Fin) para ver cómo se comportan sus medias
tercio = dias_simulados // 3

# Medias de la serie ESTACIONARIA
media_est_1 = calcular_media(serie_estacionaria[0:tercio])
media_est_2 = calcular_media(serie_estacionaria[tercio:tercio*2])
media_est_3 = calcular_media(serie_estacionaria[tercio*2:])

# Medias de la serie NO ESTACIONARIA
media_no_est_1 = calcular_media(serie_no_estacionaria[0:tercio])
media_no_est_2 = calcular_media(serie_no_estacionaria[tercio:tercio*2])
media_no_est_3 = calcular_media(serie_no_estacionaria[tercio*2:])

print("=== ANÁLISIS DEL PROCESO ESTACIONARIO ===")
print("Regla: La media debe mantenerse estable y cercana a 0 en cualquier época.")
print(f"Época 1 (Días 0-{tercio}):     Media = {media_est_1:8.3f}")
print(f"Época 2 (Días {tercio}-{tercio*2}):  Media = {media_est_2:8.3f}")
print(f"Época 3 (Días {tercio*2}-{dias_simulados}): Media = {media_est_3:8.3f}")
print("✓ Diagnóstico: ESTACIONARIO (El proceso tiene memoria a corto plazo, pero siempre vuelve a su centro).\n")

print("=== ANÁLISIS DEL PROCESO NO ESTACIONARIO (Random Walk) ===")
print("Regla: La media y la varianza vagan sin rumbo y cambian drásticamente.")
print(f"Época 1 (Días 0-{tercio}):     Media = {media_no_est_1:8.3f}")
print(f"Época 2 (Días {tercio}-{tercio*2}):  Media = {media_no_est_2:8.3f}")
print(f"Época 3 (Días {tercio*2}-{dias_simulados}): Media = {media_no_est_3:8.3f}")
print("X Diagnóstico: NO ESTACIONARIO (El proceso se desvió de su origen y no sabe cómo volver).")