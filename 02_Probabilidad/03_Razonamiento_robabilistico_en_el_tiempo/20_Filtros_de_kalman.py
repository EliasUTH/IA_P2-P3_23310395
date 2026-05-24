import random

print("=== FILTRO DE KALMAN (NAVEGACIÓN 1D) ===\n")

# --- 1. CONFIGURACIÓN DEL MUNDO Y SENSORES ---
# Varianza = Qué tanta incertidumbre/ruido hay. (A mayor número, más desconfianza)
ruido_sensor_r = 10.0   # El GPS es barato y fluctúa mucho (R)
ruido_proceso_q = 0.5   # El viento empuja un poco al dron, el movimiento no es perfecto (Q)

# --- 2. EL FILTRO DE KALMAN ---
class FiltroKalman1D:
    def __init__(self, pos_inicial, incertidumbre_inicial):
        self.x = pos_inicial  # Estimación actual del estado (Posición)
        self.p = incertidumbre_inicial  # Incertidumbre actual (P)
        
    def predecir(self, movimiento_estimado):
        """PASO 1: PREDICCIÓN (El tiempo avanza ciegamente basándose en la física)"""
        # La posición avanza según lo planeado
        self.x = self.x + movimiento_estimado
        # Al movernos a ciegas, nuestra incertidumbre CRECE por el ruido del mundo (Q)
        self.p = self.p + ruido_proceso_q
        
    def actualizar(self, medicion_sensor):
        """PASO 2: ACTUALIZACIÓN (Leemos el sensor y corregimos)"""
        # Calculamos la Ganancia de Kalman (K)
        # K se acerca a 1 si el sensor es mejor. K se acerca a 0 si nuestra predicción es mejor.
        k = self.p / (self.p + ruido_sensor_r)
        
        # Corregimos la posición: Posición Predicha + K * (Error entre Sensor y Predicción)
        self.x = self.x + k * (medicion_sensor - self.x)
        
        # Al integrar información nueva, nuestra incertidumbre DISMINUYE
        self.p = (1 - k) * self.p

# --- 3. SIMULACIÓN DEL DRON ---
dias_pasos = 15
movimiento_real_por_paso = 5.0 # El dron avanza 5 metros por segundo

# Estado inicial
posicion_real = 0.0
filtro = FiltroKalman1D(pos_inicial=0.0, incertidumbre_inicial=100.0) # Empezamos muy inseguros

print("PASO | POSICIÓN REAL | LECTURA GPS (Sensor) | ESTIMACIÓN KALMAN (IA) | INCERTIDUMBRE (P)")
print("-" * 85)

for paso in range(1, dias_pasos + 1):
    # 1. El mundo real avanza
    posicion_real += movimiento_real_por_paso
    
    # 2. El sensor GPS lee la posición, pero le mete ruido aleatorio
    error_gps = random.gauss(0, ruido_sensor_r) # Campana de Gauss
    lectura_gps = posicion_real + error_gps
    
    # 3. La IA hace su trabajo en dos fases:
    # FASE A: Predecimos que avanzamos 5 metros basándonos en nuestro acelerómetro
    filtro.predecir(movimiento_estimado=5.0)
    
    # FASE B: Leemos el GPS ruidoso y dejamos que el algoritmo fusione ambas realidades
    filtro.actualizar(medicion_sensor=lectura_gps)
    
    # 4. Resultados
    print(f"{paso:4d} | {posicion_real:13.2f}m | {lectura_gps:18.2f}m | {filtro.x:20.2f}m | {filtro.p:13.2f}")

print("\n=== ANÁLISIS DE LA INTELIGENCIA ARTIFICIAL ===")
print("1. Observa la columna del GPS: A veces se equivoca por muchos metros de diferencia.")
print("2. Observa la estimación de Kalman: Es muchísimo más suave y cercana a la Realidad,")
print("   porque no confía ciegamente en el GPS, sino que lo promedia matemáticamente")
print("   con la inercia del movimiento.")
print("3. ¡Mira la Incertidumbre (P)! Empezamos en 100.0 (totalmente perdidos), pero")
print("   conforme pasan los pasos y combinamos predicción + sensor, el algoritmo se")
print("   vuelve cada vez más seguro de dónde está, bajando la incertidumbre hasta estabilizarse.")