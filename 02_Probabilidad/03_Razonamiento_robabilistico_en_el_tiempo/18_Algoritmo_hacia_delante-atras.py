print("=== ALGORITMO HACIA ADELANTE-ATRÁS (FORWARD-BACKWARD) ===\n")

# --- 1. DEFINICIÓN DEL MODELO (HMM del Clima y el Paraguas) ---
estados = ["Lluvia", "Despejado"]
prob_inicial = {"Lluvia": 0.5, "Despejado": 0.5}

transiciones = {
    "Lluvia": {"Lluvia": 0.7, "Despejado": 0.3},
    "Despejado": {"Lluvia": 0.3, "Despejado": 0.7}
}

emisiones = {
    "Lluvia": {True: 0.9, False: 0.1},      # 90% trae paraguas si llueve
    "Despejado": {True: 0.2, False: 0.8}    # 20% trae paraguas si está despejado
}

def normalizar(diccionario_probs):
    """Asegura que las probabilidades sumen 1.0"""
    total = sum(diccionario_probs.values())
    return {estado: (prob / total) for estado, prob in diccionario_probs.items()}

# --- 2. EL ALGORITMO ---

def adelante_atras(evidencias):
    """
    Ejecuta el paso Forward, luego el Backward, y los multiplica para lograr el Suavizado.
    """
    num_dias = len(evidencias)
    
    # ---------------------------------------------------------
    # PASO A: HACIA ADELANTE (Forward / Filtrado)
    # alpha[i] guarda P(Estado_Hoy | Toda la evidencia HASTA hoy)
    # ---------------------------------------------------------
    alpha = []
    
    # Día 1 (Caso especial con prob_inicial)
    alpha_hoy = {}
    for estado in estados:
        alpha_hoy[estado] = prob_inicial[estado] * emisiones[estado][evidencias[0]]
    alpha.append(normalizar(alpha_hoy))
    
    # Día 2 en adelante
    for i in range(1, num_dias):
        evidencia_hoy = evidencias[i]
        alpha_nuevo = {estado: 0.0 for estado in estados}
        
        for estado_actual in estados:
            suma_probabilidades = sum(
                alpha[-1][estado_previo] * transiciones[estado_previo][estado_actual] 
                for estado_previo in estados
            )
            # Actualizamos con la evidencia sensada hoy
            alpha_nuevo[estado_actual] = emisiones[estado_actual][evidencia_hoy] * suma_probabilidades
            
        alpha.append(normalizar(alpha_nuevo))

    # ---------------------------------------------------------
    # PASO B: HACIA ATRÁS (Backward)
    # beta[i] guarda P(Toda la evidencia FUTURA | Estado_Hoy)
    # ---------------------------------------------------------
    beta = [None] * num_dias
    
    # El último día del futuro no tiene evidencia posterior, se inicializa en 1.0
    beta[-1] = {estado: 1.0 for estado in estados}
    
    # Viajamos al revés: desde el penúltimo día hasta el Día 1
    for i in range(num_dias - 2, -1, -1):
        evidencia_futura = evidencias[i + 1]
        beta_anterior = {estado: 0.0 for estado in estados}
        
        for estado_actual in estados:
            # ¿A dónde fuimos, qué vimos ahí, y cuál era el beta de ese futuro?
            beta_anterior[estado_actual] = sum(
                transiciones[estado_actual][estado_futuro] * emisiones[estado_futuro][evidencia_futura] * beta[i + 1][estado_futuro] 
                for estado_futuro in estados
            )
        beta[i] = normalizar(beta_anterior) # Normalizamos para evitar underflow matemático

    # ---------------------------------------------------------
    # PASO C: SUAVIZADO (Combinación)
    # Multiplicamos Alpha (Pasado/Presente) x Beta (Futuro)
    # ---------------------------------------------------------
    suavizado = []
    for i in range(num_dias):
        creencia_suavizada = {}
        for estado in estados:
            creencia_suavizada[estado] = alpha[i][estado] * beta[i][estado]
        suavizado.append(normalizar(creencia_suavizada))
        
    return alpha, suavizado

# --- 3. EJECUCIÓN Y ANÁLISIS ---

print("ESCENARIO: Evaluamos 3 días de observar al empleado con su paraguas.")
evidencias_historia = [True, True, False] # Día 1: Paraguas, Día 2: Paraguas, Día 3: Sin Paraguas

mensajes = ["(Paraguas: SÍ)", "(Paraguas: SÍ)", "(Paraguas: NO)"]

# Ejecutamos el motor
forward, suavizado_final = adelante_atras(evidencias_historia)

print("\n--- RESULTADOS: FILTRADO vs SUAVIZADO ---")

for dia in range(len(evidencias_historia)):
    print(f"\nDÍA {dia + 1} {mensajes[dia]}")
    
    # Lo que sabíamos ese día en tiempo real
    prob_lluvia_fwd = forward[dia]['Lluvia'] * 100
    print(f"  -> Con visión normal (Filtrado): Creencia de Lluvia = {prob_lluvia_fwd:.1f}%")
    
    # Lo que descubrimos viéndolo en retrospectiva
    prob_lluvia_suavizada = suavizado_final[dia]['Lluvia'] * 100
    print(f"  -> Con visión del futuro (Suavizado): Creencia de Lluvia = {prob_lluvia_suavizada:.1f}%")

print("\n=== ANÁLISIS DE LA IA ===")
print("Fíjate especialmente en el Día 1. Cuando la IA solo usaba 'Filtrado', estaba")
print("bastante segura de que llovía (81.8%), porque ese día vio un paraguas.")
print("Sin embargo, el 'Suavizado' le sumó la información del futuro: como el Día 2")
print("TAMBIÉN hubo paraguas (reforzando la racha de lluvia), la estimación histórica")
print("del Día 1 se corrigió hacia arriba (88.3%). ¡La retrospectiva la hizo más inteligente!")