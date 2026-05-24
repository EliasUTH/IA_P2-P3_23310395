print("=== RED BAYESIANA: EL PROBLEMA DE LA ALARMA ===\n")

# 1. Definimos las Tablas de Probabilidad Condicional (CPT - Conditional Probability Tables)
# Estas son las "reglas" o el conocimiento de nuestra IA.

# Nodos "Padre" (Probabilidades A Priori, no dependen de nada)
prob_robo = 0.001       # P(Robo) = 0.1% de que roben un día cualquiera
prob_terremoto = 0.002  # P(Terremoto) = 0.2% de que haya un temblor

# Nodo "Hijo" (Alarma). Depende de (Robo, Terremoto)
# Diccionario: (Hay_Robo, Hay_Terremoto) -> Probabilidad de que suene la alarma
cpt_alarma = {
    (True, True): 0.95,   # Si hay robo y terremoto, suena 95% de las veces
    (True, False): 0.94,  # Si hay robo sin terremoto, suena 94%
    (False, True): 0.29,  # Si hay terremoto sin robo, suena 29%
    (False, False): 0.001 # Si no pasa nada, suena por error el 0.1% (falsa alarma)
}

# Nodos "Nietos" (Juan y María). Solo dependen de si la Alarma suena o no.
# ¡Aquí brilla la Independencia Condicional! A Juan no le importa si hubo terremoto, solo si la alarma sonó.
cpt_juan = {
    True: 0.90,  # Si la alarma suena, Juan llama el 90% de las veces
    False: 0.05  # Si NO suena, Juan llama confundido el 5% de las veces
}

cpt_maria = {
    True: 0.70,  # Si la alarma suena, María llama el 70% de las veces (escucha música)
    False: 0.01  # Si NO suena, María casi nunca se equivoca (1%)
}

# 2. Motor de Inferencia de la Red Bayesiana
def probabilidad_estado_conjunto(robo, terremoto, alarma, juan, maria):
    """
    Calcula la probabilidad exacta de un escenario específico multiplicando
    las probabilidades de los nodos según el grafo de la Red Bayesiana.
    Regla de la Cadena: P(R, T, A, J, M) = P(R) * P(T) * P(A | R,T) * P(J | A) * P(M | A)
    """
    # 1. Obtener probabilidades de los padres
    p_R = prob_robo if robo else (1 - prob_robo)
    p_T = prob_terremoto if terremoto else (1 - prob_terremoto)
    
    # 2. Obtener probabilidad de la alarma dados los padres
    p_A = cpt_alarma[(robo, terremoto)] if alarma else (1 - cpt_alarma[(robo, terremoto)])
    
    # 3. Obtener probabilidad de los vecinos dada la alarma
    p_J = cpt_juan[alarma] if juan else (1 - cpt_juan[alarma])
    p_M = cpt_maria[alarma] if maria else (1 - cpt_maria[alarma])
    
    # La probabilidad conjunta es la multiplicación de todas (Regla de la Cadena)
    prob_total = p_R * p_T * p_A * p_J * p_M
    return prob_total

# --- ESCENARIOS PARA QUE LA IA EVALÚE ---

# Escenario 1: Suena la alarma, Juan y María llaman, pero NO hubo ni robo ni terremoto (Falsa alarma total)
escenario_1 = probabilidad_estado_conjunto(robo=False, terremoto=False, alarma=True, juan=True, maria=True)

# Escenario 2: Hay un Robo, suena la alarma, y ambos vecinos llaman (Escenario ideal)
escenario_2 = probabilidad_estado_conjunto(robo=True, terremoto=False, alarma=True, juan=True, maria=True)

print("--- EVALUACIÓN DE ESCENARIOS MUNDIALES ---")
print(f"Probabilidad de Escenario 1 (Falsa alarma, vecinos llaman): {escenario_1:.8f} ({escenario_1 * 100:.6f}%)")
print(f"Probabilidad de Escenario 2 (Robo real, vecinos llaman): {escenario_2:.8f} ({escenario_2 * 100:.6f}%)\n")

print("Conclusión de la IA:")
print("- Aunque el Escenario 2 (Robo) parece más 'lógico' humanamente,")
print("- Matemáticamente el Escenario 1 es MUCHO más probable de que ocurra en la vida real.")
print("- Razón: Los robos son extremadamente raros (0.1%), por lo que es más común")
print("  que la alarma falle y los vecinos llamen por error, a que realmente te roben.")