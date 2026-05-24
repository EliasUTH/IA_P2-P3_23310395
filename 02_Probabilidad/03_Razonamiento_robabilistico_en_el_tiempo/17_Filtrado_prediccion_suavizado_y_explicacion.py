print("=== INFERENCIA EN MODELOS OCULTOS DE MARKOV (HMM) ===\n")

# --- 1. DEFINICIÓN DEL MODELO (El mundo del Paraguas) ---
estados = ["Lluvia", "Despejado"]

# P(X_0): Probabilidad el día 0
prob_inicial = {"Lluvia": 0.5, "Despejado": 0.5}

# P(X_t+1 | X_t): Matriz de transición (El clima de mañana dado el clima de hoy)
transiciones = {
    "Lluvia": {"Lluvia": 0.7, "Despejado": 0.3},
    "Despejado": {"Lluvia": 0.3, "Despejado": 0.7}
}

# P(E_t | X_t): Matriz de Emisión/Sensor (Probabilidad de ver un paraguas dado el clima)
emisiones = {
    "Lluvia": {True: 0.9, False: 0.1},      # Si llueve, 90% seguro trae paraguas
    "Despejado": {True: 0.2, False: 0.8}    # Si está despejado, 20% trae paraguas por si acaso
}

def normalizar(diccionario_probs):
    """Asegura que las probabilidades sumen 1.0"""
    total = sum(diccionario_probs.values())
    return {estado: (prob / total) for estado, prob in diccionario_probs.items()}

# --- 2. LOS 4 ALGORITMOS FUNDAMENTALES ---

def filtrado(creencia_previa, evidencia_hoy):
    """
    Calcula P(Estado_Hoy | Toda_la_evidencia_hasta_hoy).
    Avanza un día y ajusta la creencia según el sensor.
    """
    # Paso A: Predicción (Avanzamos un día ciegamente)
    prediccion = {estado: 0.0 for estado in estados}
    for estado_nuevo in estados:
        for estado_viejo in estados:
            prediccion[estado_nuevo] += transiciones[estado_viejo][estado_nuevo] * creencia_previa[estado_viejo]
            
    # Paso B: Actualización (Cruzamos la predicción con lo que ven nuestros ojos)
    actualizacion = {estado: 0.0 for estado in estados}
    for estado in estados:
        actualizacion[estado] = prediccion[estado] * emisiones[estado][evidencia_hoy]
        
    return normalizar(actualizacion)

def prediccion_futura(creencia_actual, dias_futuros):
    """
    Calcula P(Estado_Futuro | Evidencia_Actual).
    Avanza varios días en el tiempo SIN nueva evidencia (porque es el futuro).
    """
    creencia = creencia_actual.copy()
    for _ in range(dias_futuros):
        nueva_creencia = {estado: 0.0 for estado in estados}
        for estado_nuevo in estados:
            for estado_viejo in estados:
                nueva_creencia[estado_nuevo] += transiciones[estado_viejo][estado_nuevo] * creencia[estado_viejo]
        creencia = nueva_creencia # No normalizamos aquí porque sin evidencia, las transiciones ya suman 1
    return creencia

def explicacion_viterbi(secuencia_evidencias):
    """
    Encuentra la SECUENCIA EXACTA MÁS PROBABLE que explique los datos (Algoritmo de Viterbi).
    """
    # Guarda el mejor camino para llegar a cada estado: {estado: (prob_acumulada, [camino_historico])}
    evidencia_inicial = secuencia_evidencias[0]
    caminos = {
        estado: (prob_inicial[estado] * emisiones[estado][evidencia_inicial], [estado]) 
        for estado in estados
    }
    
    # Normalizamos el primer día para evitar que los números se vuelvan microscópicos (Underflow)
    probs_normalizadas = normalizar({k: v[0] for k, v in caminos.items()})
    caminos = {estado: (probs_normalizadas[estado], caminos[estado][1]) for estado in estados}

    # Procesamos desde el día 2 en adelante
    for ev in secuencia_evidencias[1:]:
        nuevos_caminos = {}
        for estado_actual in estados:
            mejor_prob = -1
            mejor_camino = []
            
            # Revisamos desde qué estado del ayer es mejor haber venido
            for estado_previo in estados:
                prob_previa = caminos[estado_previo][0]
                camino_previo = caminos[estado_previo][1]
                
                # Fórmula Viterbi: Prob Previa * Transición * Emisión
                prob_transicion = transiciones[estado_previo][estado_actual]
                prob_emision = emisiones[estado_actual][ev]
                prob_candidata = prob_previa * prob_transicion * prob_emision
                
                if prob_candidata > mejor_prob:
                    mejor_prob = prob_candidata
                    mejor_camino = camino_previo + [estado_actual]
                    
            nuevos_caminos[estado_actual] = (mejor_prob, mejor_camino)
            
        # Normalizamos los puntajes del día
        suma_probs = sum(c[0] for c in nuevos_caminos.values())
        caminos = {estado: (val[0] / suma_probs, val[1]) for estado, val in nuevos_caminos.items()}
        
    # De los estados finales, elegimos el que tenga mayor probabilidad
    estado_ganador = max(caminos.keys(), key=lambda k: caminos[k][0])
    return caminos[estado_ganador][1]

# --- EJECUCIÓN DEL CASO PRÁCTICO ---

print("ESCENARIO: Un jefe no tiene ventanas. Observa si el guardia trae paraguas 3 días seguidos.")
# Día 1: Sí trae, Día 2: Sí trae, Día 3: NO trae
evidencias_historia = [True, True, False]

print(f"Evidencia observada: Día 1 (Paraguas={evidencias_historia[0]}), Día 2 (Paraguas={evidencias_historia[1]}), Día 3 (Paraguas={evidencias_historia[2]})\n")

# 1. FILTRADO (Día por Día)
print("1. FILTRADO (¿En qué clima estamos cada día?)")
creencia = prob_inicial
historial_filtrado = []

for dia, paraguas_hoy in enumerate(evidencias_historia):
    creencia = filtrado(creencia, paraguas_hoy)
    historial_filtrado.append(creencia)
    prob_lluvia = creencia['Lluvia'] * 100
    print(f"   Día {dia+1} - Creencia de Lluvia: {prob_lluvia:.1f}%")

print("\n2. PREDICCIÓN (Mirando hacia el futuro)")
# Situados en el día 3, ¿qué pasará en el día 5 (2 días después)?
creencia_dia_5 = prediccion_futura(historial_filtrado[-1], 2)
prob_lluvia_d5 = creencia_dia_5['Lluvia'] * 100
print(f"   Estando en el Día 3, la IA predice para el Día 5: {prob_lluvia_d5:.1f}% de Lluvia.")
print("   (Nota: Sin nueva evidencia, la predicción tiende lentamente a estacionarse en 50/50)\n")

print("3. SUAVIZADO (Mejorando el pasado)")
# En el filtrado, el Día 1 solo tenía información del Día 1. 
# En Suavizado, el Día 1 se beneficia de saber que llovió el Día 2.
print("   Nota conceptual: El algoritmo completo Forward-Backward usaría el historial de")
print("   evidencias para corregir retrospectivamente la creencia del Día 1. A menudo,")
print("   saber qué pasó después, aclara nuestras dudas sobre qué estaba pasando antes.\n")

print("4. EXPLICACIÓN (Algoritmo de Viterbi)")
mejor_historia = explicacion_viterbi(evidencias_historia)
historia_formateada = ' -> '.join(mejor_historia)
print(f"   La IA dice que la secuencia exacta de climas que mejor explica los paraguas es:")
print(f"   {historia_formateada}")