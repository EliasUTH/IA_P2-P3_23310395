import random

print("=== GENERADOR DE MODELOS OCULTOS DE MARKOV (HMM) ===\n")

# --- 1. DEFINICIÓN DEL MUNDO ---
# (Seguimos con el universo del Clima y los Paraguas para mantener la consistencia)

prob_inicial = {"Lluvia": 0.5, "Despejado": 0.5}

# La Cadena de Markov (La verdad que fluye en secreto)
transiciones = {
    "Lluvia": {"Lluvia": 0.7, "Despejado": 0.3},
    "Despejado": {"Lluvia": 0.3, "Despejado": 0.7}
}

# El Modelo del Sensor (Cómo la verdad se manifiesta en el mundo físico)
emisiones = {
    "Lluvia": {"Paraguas": 0.9, "Sin Paraguas": 0.1},
    "Despejado": {"Paraguas": 0.2, "Sin Paraguas": 0.8}
}

# --- 2. EL MOTOR DE SIMULACIÓN ---
def generar_secuencia_hmm(dias):
    """
    Simula el paso del tiempo en un HMM.
    Devuelve dos líneas de tiempo: La verdad absoluta y las pistas observables.
    """
    historia_oculta = []
    historia_visible = []
    
    # El mundo se crea en el Día 1 usando las probabilidades iniciales
    # random.choices devuelve una lista, tomamos el elemento [0]
    estado_actual = random.choices(
        list(prob_inicial.keys()), 
        weights=list(prob_inicial.values())
    )[0]
    
    for dia in range(dias):
        # PASO A: El estado actual emite una señal (Observación)
        probs_emision = emisiones[estado_actual]
        observacion_actual = random.choices(
            list(probs_emision.keys()),
            weights=list(probs_emision.values())
        )[0]
        
        # Guardamos los registros en los anales de la historia
        historia_oculta.append(estado_actual)
        historia_visible.append(observacion_actual)
        
        # PASO B: El tiempo avanza (Transición al clima de mañana)
        probs_transicion = transiciones[estado_actual]
        estado_actual = random.choices(
            list(probs_transicion.keys()),
            weights=list(probs_transicion.values())
        )[0]
        
    return historia_oculta, historia_visible

# --- 3. EJECUCIÓN Y ANÁLISIS ---

dias_a_simular = 15
print(f"Creando un mundo virtual de {dias_a_simular} días...\n")

realidad, percepcion = generar_secuencia_hmm(dias_a_simular)

print("DÍA | REALIDAD OCULTA | LO QUE VEN NUESTROS OJOS")
print("-" * 52)
for i in range(dias_a_simular):
    print(f"{i+1:2d}  | {realidad[i]:<15} | {percepcion[i]}")

print("\n=== LA PERSPECTIVA DE LA INTELIGENCIA ARTIFICIAL ===")
print("Este script actúa como el universo mismo: conoce perfectamente")
print("la columna de 'Realidad Oculta', pero solo nos permite ver la")
print("columna de la derecha.")
print("\nEl verdadero reto en el Machine Learning no es ejecutar este")
print("código, sino hacer lo inverso: Tomar únicamente la lista de")
print("paraguas e intentar reconstruir la columna central usando algoritmos")
print("como Viterbi (que programaste un par de archivos atrás).")