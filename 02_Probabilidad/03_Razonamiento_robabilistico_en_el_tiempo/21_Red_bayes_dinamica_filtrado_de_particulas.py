import random

print("=== FILTRADO DE PARTÍCULAS (RED BAYESIANA DINÁMICA) ===\n")

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
NUM_PARTICULAS = 500
LONGITUD_PASILLO = 100.0  # El robot vive en un mundo de 0 a 100 metros
RUIDO_MOVIMIENTO = 1.0    # Qué tanto se desvía el robot al caminar
RUIDO_SENSOR = 2.0        # Margen de error del sensor de distancia

# --- 2. EL ALGORITMO DE PARTÍCULAS ---

class FiltroParticulas:
    def __init__(self, num_p):
        # Inicializamos partículas en posiciones aleatorias del pasillo
        self.particulas = [random.uniform(0, LONGITUD_PASILLO) for _ in range(num_p)]
        self.pesos = [1.0 / num_p] * num_p

    def predecir(self, movimiento):
        """Mueve cada partícula y le añade ruido (Incertidumbre del movimiento)"""
        nuevas_p = []
        for p in self.particulas:
            # Cada partícula intenta seguir al robot pero con su propio error
            salto = movimiento + random.gauss(0, RUIDO_MOVIMIENTO)
            nuevas_p.append((p + salto) % LONGITUD_PASILLO) # Mundo circular para el ejemplo
        self.particulas = nuevas_p

    def actualizar(self, medicion_robot):
        """Asigna pesos según qué tan cerca está cada partícula de la realidad medida"""
        nuevos_pesos = []
        for p in self.particulas:
            # Calculamos la probabilidad (Gaussiana) de que la partícula 'p' 
            # sea la posición real dada la medición
            error = abs(p - medicion_robot)
            # Función de peso simple: entre menor error, mayor peso
            peso = 1.0 / (error + 0.1) 
            nuevos_pesos.append(peso)
        
        # Normalizamos los pesos para que sumen 1
        total = sum(nuevos_pesos)
        self.pesos = [w / total for w in nuevos_pesos]

    def resample(self):
        """Las partículas con más peso sobreviven y se multiplican"""
        # Método de la 'Rueda de la Fortuna'
        nuevas_particulas = random.choices(
            self.particulas, 
            weights=self.pesos, 
            k=NUM_PARTICULAS
        )
        self.particulas = nuevas_particulas
        self.pesos = [1.0 / NUM_PARTICULAS] * NUM_PARTICULAS

    def estimar_posicion(self):
        """La posición estimada es el promedio de todas las partículas"""
        return sum(self.particulas) / len(self.particulas)

# --- 3. SIMULACIÓN ---

filtro = FiltroParticulas(NUM_PARTICULAS)
posicion_real = 20.0 # El robot empieza en el metro 20
movimiento_paso = 5.0

print(f"{'PASO':<5} | {'REAL':<10} | {'ESTIMADA':<12} | {'ERROR':<10}")
print("-" * 45)

for paso in range(1, 11):
    # 1. El robot se mueve
    posicion_real = (posicion_real + movimiento_paso) % LONGITUD_PASILLO
    
    # 2. El sensor mide (con ruido)
    medicion = posicion_real + random.gauss(0, RUIDO_SENSOR)
    
    # 3. El Filtro trabaja
    filtro.predecir(movimiento_paso)
    filtro.actualizar(medicion)
    filtro.resample() # El paso clave
    
    estimacion = filtro.estimar_posicion()
    error_final = abs(posicion_real - estimacion)
    
    print(f"{paso:<5} | {posicion_real:8.2f}m | {estimacion:10.2f}m | {error_final:8.2f}m")

print("\n=== ANÁLISIS DEL FILTRADO DE PARTÍCULAS ===")
print("Este algoritmo es una 'Simulación de Monte Carlo'. Nota cómo al principio")
print("las partículas están dispersas, pero tras unos pocos pasos de 'Resampling',")
print("la IA descarta las hipótesis falsas y las partículas se aglutinan")
print("alrededor de la posición real del robot.")